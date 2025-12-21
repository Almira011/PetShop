from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    region = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    vaccinated = models.BooleanField(default=False)
    sterilized = models.BooleanField(default=False)
    features = models.TextField(blank=True)
    shelter = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    info = models.TextField(blank=True)


    def __str__(self):
        return self.name
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="customer_profile"
    )
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    address = models.TextField()

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="orders"
    )
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.id} - {self.customer.name}"


class OrderProduct(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="order_products"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="order_products"
    )

    class Meta:
        unique_together = ('order', 'product')

    def __str__(self):
        return f"Order {self.order.id} - {self.product.name}"