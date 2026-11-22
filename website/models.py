from django.db import models
from django.conf import settings

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=50, unique=True)
    barcode = models.CharField(max_length=100, unique=True, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    low_stock_alert = models.IntegerField(default=5)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.sku}"

    @property
    def is_low_stock(self):
        return self.stock <= self.low_stock_alert

class StockMovement(models.Model):
    IN = 'IN'
    OUT = 'OUT'
    TYPES = [(IN, 'Stock In'), (OUT, 'Stock Out')]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    movement_type = models.CharField(max_length=3, choices=TYPES)
    quantity = models.IntegerField()
    note = models.CharField(max_length=255, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[('PENDING', 'Pending'), ('APPROVED', 'Approved')],
        default='PENDING',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_amount(self):
        return self.product.price * self.quantity

class PortfolioRating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user'], name='unique_portfolio_rating_per_user')
        ]

    def __str__(self):
        return f'{self.user.username}: {self.rating}/5'

class CustomerOrder(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer_orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=30)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order #{self.id} - {self.customer.username}'

    @property
    def total_amount(self):
        return sum(item.total_amount for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(CustomerOrder, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.product.name} x {self.quantity}'

    @property
    def total_amount(self):
        return self.product.price * self.quantity

class Tile(models.Model):
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    size = models.CharField(max_length=50)
    material = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    finish = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image_url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class TileShopOrder(models.Model):
    customer_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=30, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order #{self.id} - {self.customer_name}'


class TileShopOrderItem(models.Model):
    order = models.ForeignKey(TileShopOrder, on_delete=models.CASCADE, related_name='items')
    tile = models.ForeignKey(Tile, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.tile.name} x {self.quantity}'