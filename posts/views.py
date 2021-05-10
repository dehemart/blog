from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from .models import Post
from django.db.models import Q, Count, Case, When
from comentarios.forms import FormComentario
from comentarios.models import Comentario
from django.contrib import messages
from django.views import View
from django.conf import settings


class PostIndex(ListView):
    model = Post
    template_name = 'posts/index.html'
    paginate_by = 3
    context_object_name = 'posts'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related('categoria_post')
        qs = qs.order_by('-id').filter(publicado_post=True)
        qs = qs.annotate(
            total_comentarios=Count(
                Case(
                    When(
                        comentario__publicado_comentario=True, then=1
                    )
                )
            )
        )

        return qs


class PostBusca(PostIndex):
    template_name = 'posts/post_busca.html'

    def get_queryset(self):
        qs = super().get_queryset()
        termo = self.request.GET.get('termo')

        qs = qs.filter(
            Q(titulo_post__icontains=termo) |
            Q(autor_post__first_name__iexact=termo) |
            Q(conteudo_post__icontains=termo) |
            Q(excerto_post__icontains=termo) |
            Q(categoria_post__nome_cat__iexact=termo)
        )

        return qs


class PostCategoria(PostIndex):
    template_name = 'posts/post_categoria.html'

    def get_queryset(self):
        qs = super().get_queryset()

        print(self.kwargs)

        categoria = self.kwargs.get('categoria', None)

        if not categoria:
            return qs

        qs = qs.filter(categoria_post__nome_cat__iexact=categoria)

        return qs


class PostDetalhes(View):
    template_name = 'posts/post_detalhes.html'

    def setup(self, request, *args, **kwargs):
        super().setup(self, request, *args, **kwargs)

        pk = self.kwargs.get('pk')
        post = get_object_or_404(Post, pk=pk, publicado_post=True)
        self.contexto = {
            'post': post,
            'comentarios': Comentario.objects.filter(post_comentario=post,
                                                     publicado_comentario=True),
            'form': FormComentario(request.POST or None),
        }

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.contexto)

    def post(self, request, *args, **kwargs):
        form = self.contexto['form']
        if not form.is_valid():
            return render(request, self.template_name, self.contexto)

        comentario = form.save(commit=False)

        if request.user.is_authenticated:
            comentario.usuario_comentario = request.user

        comentario.post_comentario = self.contexto['post']
        comentario.save()

        messages.success(request, 'Comentário enviado para aprovação.')

        return redirect('post_detalhes', pk=self.kwargs.get('pk'))

    def save(self, *args, **kwargs):
        super().save
        self.image_resize(self.imagem_post.name, 800, 60)

    @staticmethod
    def image_resize(image_name, new_width, quality):
        image_path = os.path.join(settings.MEDIA_ROOT, image_name)

        img = Image.open(image_path)
        width, height = img.size

        new_height = round((new_width * height) / width)

        if width <= new_width:
            img.close()
            return

        new_img = img.resize((new_height, new_height), Image.ANTIALIAS)
        new_img.save(image_path, optmize=True, quality=quality)
        new_img.close()
