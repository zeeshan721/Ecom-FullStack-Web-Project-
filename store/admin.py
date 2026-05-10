from django.contrib import admin
from .models import Contact,UserProfile,Product,Review,Cart,CartItem,Order,OrderItem,Wishlist

# Register your models here.
admin.site.register(Contact)
admin.site.register(UserProfile)
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Wishlist)
@property
def full_name(self):
    return f"{self.first_name} {self.last_name}"