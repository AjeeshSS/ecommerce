from django.contrib import admin
from .models.product import Product
from .models.category import Category
from .models.customer import Customer
from .models.our_user import Our_user
from .models.cart import Cart

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Our_user)
admin.site.register(Cart)
