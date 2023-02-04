from django.db import models
from .category import Category


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    stoke = models.IntegerField(default=0)
    description = models.CharField(max_length=200, default='', null=True, blank=True)
    brand = models.CharField(max_length=500)
    image = models.ImageField(upload_to='productImages/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default='men')
    colour_variant = models.CharField(max_length=50,blank=True)
    size_variant = models.CharField(max_length=50,blank=True)

    def __str__(self):
        return self.name

  

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Product.objects.filter(category=category_id)
        else:
            return Product.objects.all()
