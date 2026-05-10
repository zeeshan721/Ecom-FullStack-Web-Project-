from django.db import models
from django.conf import settings
from django.utils.text import slugify


# ===========================
# CONTACT
# ===========================
class Contact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name  = models.CharField(max_length=100)
    email      = models.EmailField()
    subject    = models.CharField(max_length=200)
    message    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.subject}"


# ===========================
# USER PROFILE
# ===========================
class UserProfile(models.Model):
    user     = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    phone    = models.CharField(max_length=20, blank=True)
    address  = models.TextField(blank=True)
    city     = models.CharField(max_length=100, blank=True)
    province = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"


# ===========================
# PRODUCT
# ===========================
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('clothing',  'Clothing'),
        ('shoes',     'Shoes'),
        ('cosmetics', 'Cosmetics'),
    ]

    name         = models.CharField(max_length=200)
    slug         = models.SlugField(unique=True, blank=True)
    category     = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    sub_category = models.CharField(max_length=100, blank=True)
    description  = models.TextField(blank=True)
    price        = models.DecimalField(max_digits=10, decimal_places=2)
    old_price    = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image        = models.ImageField(upload_to='products/', blank=True, null=True)
    stock        = models.PositiveIntegerField(default=0)
    is_new       = models.BooleanField(default=False)
    is_sale      = models.BooleanField(default=False)
    is_featured  = models.BooleanField(default=False)
    rating       = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    created_at   = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def discount_percent(self):
        if self.old_price and self.old_price > self.price:
            return int(((self.old_price - self.price) / self.old_price) * 100)
        return 0

    @property
    def in_stock(self):
        return self.stock > 0


# ===========================
# PRODUCT REVIEW
# ===========================
class Review(models.Model):
    product    = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating     = models.PositiveIntegerField(default=5)
    comment    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} → {self.product.name} ({self.rating}★)"


# ===========================
# CART
# ===========================
class Cart(models.Model):
    user       = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

    @property
    def total(self):
        return sum(item.subtotal for item in self.items.all())

    @property
    def item_count(self):
        return self.items.count()


class CartItem(models.Model):
    cart     = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size     = models.CharField(max_length=20, blank=True)
    color    = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"

    @property
    def subtotal(self):
        return self.product.price * self.quantity


# ===========================
# ORDER
# ===========================
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending',    'Pending'),
        ('processing', 'Processing'),
        ('shipped',    'Shipped'),
        ('delivered',  'Delivered'),
        ('cancelled',  'Cancelled'),
    ]

    PAYMENT_CHOICES = [
        ('cod',       'Cash on Delivery'),
        ('easypaisa', 'EasyPaisa / JazzCash'),
        ('card',      'Credit / Debit Card'),
        ('bank',      'Bank Transfer'),
    ]

    user           = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    status         = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='cod')

    # Shipping Info
    first_name = models.CharField(max_length=100)
    last_name  = models.CharField(max_length=100)
    email      = models.EmailField()
    phone      = models.CharField(max_length=20)
    address    = models.TextField()
    city       = models.CharField(max_length=100)
    province   = models.CharField(max_length=100)
    postal     = models.CharField(max_length=20, blank=True)
    notes      = models.TextField(blank=True)

    total      = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} — {self.user.username}"

    def calculate_total(self):
        self.total = sum(item.subtotal for item in self.order_items.all())
        self.save()


class OrderItem(models.Model):
    order    = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price    = models.DecimalField(max_digits=10, decimal_places=2)
    size     = models.CharField(max_length=20, blank=True)
    color    = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"

    @property
    def subtotal(self):
        return self.price * self.quantity


# ===========================
# WISHLIST
# ===========================
class Wishlist(models.Model):
    user     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlist')
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} ♥ {self.product.name}"