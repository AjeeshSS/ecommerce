from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=50)
    phone = models.BigIntegerField()
    email = models.EmailField()
    password = models.CharField(max_length=500)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name



    @staticmethod
    def get_all_customers():
        return Customer.objects.all()

    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False
