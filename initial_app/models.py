from django.db import models
from django.contrib.auth.models import User

class Products(models.Model):
    ''' Where all the products are listed'''
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='products/images/')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.name[:20]}...'


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_user')
    item = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='cart_item')
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.item.name
    



STATUS_CHOICES = (
("PENDING", "Pending"),
("PAID", "Paid"),
("FAILED", "Failed"),
)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stripe_session_id = models.CharField(max_length=255, unique=True)
    total_amount = models.DecimalField(max_digits=10,decimal_places=2) 
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"


class OrderItemHistory(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"