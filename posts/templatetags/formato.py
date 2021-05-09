from django import template

register = template.Library()


@register.filter(name='unidade_comentario')
def unidade_compentario(numero_comentarios):
    try:
        numero_comentarios = int(numero_comentarios)
        if numero_comentarios == 1:
            return f'{numero_comentarios} comentário'
        elif numero_comentarios > 1:
            return f'{numero_comentarios} comentários'

    except:
        pass

    return f'sem comentários'
