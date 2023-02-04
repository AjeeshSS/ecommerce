from django.db import models
from .customer import Customer
from .product import Product


class Cart(models.Model):
    name = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='carts')



   

    

    
