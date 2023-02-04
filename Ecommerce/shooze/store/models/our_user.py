from django.db import models


class Our_user(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    pincode = models.IntegerField()
    phone = models.IntegerField()
    email = models.EmailField()
    landmark =  models.CharField(max_length=50)
    city = models.CharField(max_length=50,default='Trivandrum')
    state = models.CharField(max_length=50, default='state')
    
    def __str__(self):
        return self.name

    @staticmethod
    def get_all_our_users():
        return Our_user.objects.all()

   
