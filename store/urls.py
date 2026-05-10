from django.urls import path
from . import views

urlpatterns = [

    # Main Pages
    path('',        views.index,   name='home'),
    path('about/',  views.about,   name='about'),
    path('contact/', views.contact, name='contact'),

    # Listing Pages
    path('clothing/',  views.clothing,  name='clothing'),
    path('shoes/',     views.shoes,     name='shoes'),
    path('cosmetics/', views.cosmetics, name='cosmetics'),

    # Product
    path('product/<slug:slug>/',        views.product_detail, name='product_detail'),
    path('product/quick-view/<int:product_id>/', views.quick_view, name='quick_view'),

    # Cart
    path('cart/',                      views.cart,             name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart,      name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart,      name='update_cart'),

    # Checkout & Order
    path('checkout/',      views.checkout,      name='checkout'),
    path('order-success/', views.order_success, name='order_success'),

    # Wishlist
    path('wishlist/toggle/<int:product_id>/', views.toggle_wishlist, name='toggle_wishlist'),

    # Profile
    path('profile/',         views.profile,         name='profile'),
    path('password-change/', views.password_change, name='password_change'),
]