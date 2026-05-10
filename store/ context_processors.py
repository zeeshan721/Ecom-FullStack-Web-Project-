from .models import Cart


def cart_context(request):
    """
    Har page pe cart count available hoga navbar mein
    base.html mein {{ cart_count }} se use kar sako
    """
    cart_count = 0
    cart = None

    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_count = cart.item_count
        except Cart.DoesNotExist:
            pass

    return {
        'cart_count': cart_count,
        'cart_obj':   cart,
    }