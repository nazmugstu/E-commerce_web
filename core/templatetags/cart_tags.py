from django import template

register = template.Library()

@register.simple_tag
def cart_item_count(request):
    """ব্যবহারকারীর কার্টে আইটেমের সংখ্যা প্রদর্শন করে"""
    if not request.user.is_authenticated:
        return 0
    cart = request.user.cart
    return cart.items.count()