from django.db import models

from user.models import User


class Product(models.Model):
    name = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    description = models.TextField(max_length=1500)
    price = models.IntegerField()

    def __str__(self):
        return f'{self.name} {self.price} {self.pk}'


class Cart(models.Model):
    products = models.ManyToManyField(Product, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Order(models.Model):
    products = models.ManyToManyField(Cart)
    order_price = models.IntegerField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
