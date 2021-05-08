from categorias.models import Categoria


def show_categoria_menu(context):
    cat_menu = Categoria.objects.all()

    return {'cat_menu': cat_menu}
