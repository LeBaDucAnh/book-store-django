from django import template

register = template.Library()

@register.filter(name='is_in_cart')
def is_in_cart(book, cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == book.id:
            return True
    return False