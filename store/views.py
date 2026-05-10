from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.http import JsonResponse
from .models import (
    Product, Review, Cart, CartItem,
    Order, OrderItem, Wishlist, UserProfile
)


# ===========================
# HOME
# ===========================
def index(request):
    featured     = Product.objects.filter(is_featured=True)[:8]
    new_arrivals = Product.objects.filter(is_new=True)[:4]
    return render(request, 'index.html', {
        'products':     featured,
        'new_arrivals': new_arrivals,
    })


# ===========================
# ABOUT
# ===========================
def about(request):
    return render(request, 'about.html')


# ===========================
# CONTACT
# ===========================
def contact(request):
    from .models import Contact
    if request.method == 'POST':
        Contact.objects.create(
            first_name = request.POST.get('first_name', ''),
            last_name  = request.POST.get('last_name',  ''),
            email      = request.POST.get('email',      ''),
            subject    = request.POST.get('subject',    ''),
            message    = request.POST.get('message',    ''),
        )
        messages.success(request, 'Message sent!')
        return redirect('contact')
    return render(request, 'contact.html')


# ===========================
# LISTING PAGES
# ===========================
def clothing(request):
    products  = Product.objects.filter(category='clothing')
    sub_cat   = request.GET.getlist('cat')
    max_price = request.GET.get('max_price')
    sort      = request.GET.get('sort', 'newest')
    if sub_cat:
        products = products.filter(sub_category__in=sub_cat)
    if max_price:
        products = products.filter(price__lte=max_price)
    if sort == 'price-low':
        products = products.order_by('price')
    elif sort == 'price-high':
        products = products.order_by('-price')
    elif sort == 'popular':
        products = products.order_by('-rating')
    else:
        products = products.order_by('-created_at')
    return render(request, 'clothing.html', {'products': products})


def shoes(request):
    products  = Product.objects.filter(category='shoes')
    sub_cat   = request.GET.getlist('type')
    max_price = request.GET.get('max_price')
    sort      = request.GET.get('sort', 'newest')
    if sub_cat:
        products = products.filter(sub_category__in=sub_cat)
    if max_price:
        products = products.filter(price__lte=max_price)
    if sort == 'price-low':
        products = products.order_by('price')
    elif sort == 'price-high':
        products = products.order_by('-price')
    elif sort == 'popular':
        products = products.order_by('-rating')
    else:
        products = products.order_by('-created_at')
    return render(request, 'shoes.html', {'products': products})


def cosmetics(request):
    products  = Product.objects.filter(category='cosmetics')
    sub_cat   = request.GET.getlist('cat')
    max_price = request.GET.get('max_price')
    sort      = request.GET.get('sort', 'newest')
    if sub_cat:
        products = products.filter(sub_category__in=sub_cat)
    if max_price:
        products = products.filter(price__lte=max_price)
    if sort == 'price-low':
        products = products.order_by('price')
    elif sort == 'price-high':
        products = products.order_by('-price')
    elif sort == 'popular':
        products = products.order_by('-rating')
    else:
        products = products.order_by('-created_at')
    return render(request, 'cosmetics.html', {'products': products})


# ===========================
# PRODUCT DETAIL
# ===========================
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    reviews = product.reviews.all().order_by('-created_at')
    related = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id)[:4]

    if request.method == 'POST' and request.user.is_authenticated:
        Review.objects.create(
            product = product,
            user    = request.user,
            rating  = request.POST.get('rating', 5),
            comment = request.POST.get('comment', ''),
        )
        messages.success(request, 'Review submitted!')
        return redirect('product_detail', slug=slug)

    return render(request, 'product_detail.html', {
        'product': product,
        'reviews': reviews,
        'related': related,
    })


# ===========================
# QUICK VIEW — AJAX
# ===========================
def quick_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    data = {
        'id':           product.id,
        'name':         product.name,
        'slug':         product.slug,
        'price':        str(product.price),
        'old_price':    str(product.old_price) if product.old_price else None,
        'description':  product.description,
        'sub_category': product.sub_category,
        'category':     product.category,
        'rating':       str(product.rating),
        'is_new':       product.is_new,
        'is_sale':      product.is_sale,
        'in_stock':     product.in_stock,
        'image':        product.image.url if product.image else None,
    }
    return JsonResponse(data)


# ===========================
# CART
# ===========================
@login_required
def cart(request):
    cart_obj, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart.html', {'cart': cart_obj})


@login_required
def add_to_cart(request, product_id):
    product     = get_object_or_404(Product, id=product_id)
    cart_obj, _ = Cart.objects.get_or_create(user=request.user)
    size        = request.POST.get('size', '')
    color       = request.POST.get('color', '')
    quantity    = int(request.POST.get('quantity', 1))

    item, created = CartItem.objects.get_or_create(
        cart    = cart_obj,
        product = product,
        size    = size,
        color   = color,
    )
    if not created:
        item.quantity += quantity
    else:
        item.quantity = quantity
    item.save()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'message':    f'{product.name} added to cart!',
            'cart_count': cart_obj.item_count,
        })

    messages.success(request, f'{product.name} added to cart! 🛍')
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def remove_from_cart(request, item_id):
    item     = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    cart_obj = Cart.objects.get(user=request.user)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'message':    'Item removed',
            'cart_count': cart_obj.item_count,
        })
    return redirect('cart')


@login_required
def update_cart(request, item_id):
    item     = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    quantity = int(request.POST.get('quantity', 1))

    if quantity < 1:
        item.delete()
    else:
        item.quantity = quantity
        item.save()

    cart_obj = Cart.objects.get(user=request.user)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'subtotal':   str(item.subtotal) if quantity >= 1 else '0',
            'cart_total': str(cart_obj.total),
            'cart_count': cart_obj.item_count,
        })
    return redirect('cart')


# ===========================
# CHECKOUT
# ===========================
@login_required
def checkout(request):
    cart_obj = get_object_or_404(Cart, user=request.user)

    if cart_obj.items.count() == 0:
        messages.warning(request, 'Your cart is empty!')
        return redirect('cart')

    if request.method == 'POST':
        order = Order.objects.create(
            user           = request.user,
            payment_method = request.POST.get('payment', 'cod'),
            first_name     = request.POST.get('first_name', ''),
            last_name      = request.POST.get('last_name',  ''),
            email          = request.POST.get('email',      ''),
            phone          = request.POST.get('phone',      ''),
            address        = request.POST.get('address',    ''),
            city           = request.POST.get('city',       ''),
            province       = request.POST.get('province',   ''),
            postal         = request.POST.get('postal',     ''),
            notes          = request.POST.get('notes',      ''),
        )
        for item in cart_obj.items.all():
            OrderItem.objects.create(
                order    = order,
                product  = item.product,
                quantity = item.quantity,
                price    = item.product.price,
                size     = item.size,
                color    = item.color,
            )
        order.calculate_total()
        cart_obj.items.all().delete()
        request.session['last_order_id'] = order.id
        messages.success(request, 'Order placed successfully!')
        return redirect('order_success')

    return render(request, 'checkout.html', {'cart': cart_obj})


# ===========================
# ORDER SUCCESS
# ===========================
@login_required
def order_success(request):
    order_id = request.session.get('last_order_id')
    order    = get_object_or_404(Order, id=order_id, user=request.user) if order_id else None
    return render(request, 'order_success.html', {'order': order})


# ===========================
# WISHLIST
# ===========================
@login_required
def toggle_wishlist(request, product_id):
    product      = get_object_or_404(Product, id=product_id)
    obj, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    if not created:
        obj.delete()
        return JsonResponse({'status': 'removed'})
    return JsonResponse({'status': 'added'})


# ===========================
# PROFILE
# ===========================
@login_required
def profile(request):
    orders      = request.user.orders.all().order_by('-created_at')
    wishlist    = request.user.wishlist.all()
    profile_obj, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user            = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name  = request.POST.get('last_name',  user.last_name)
        user.email      = request.POST.get('email',      user.email)
        user.save()
        profile_obj.phone    = request.POST.get('phone',    profile_obj.phone)
        profile_obj.city     = request.POST.get('city',     profile_obj.city)
        profile_obj.province = request.POST.get('province', profile_obj.province)
        profile_obj.save()
        messages.success(request, 'Profile updated!')
        return redirect('profile')

    return render(request, 'profile.html', {
        'orders':   orders,
        'wishlist': wishlist,
        'profile':  profile_obj,
    })


# ===========================
# PASSWORD CHANGE
# ===========================
@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Password updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please fix the errors.')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'profile.html', {'form': form})