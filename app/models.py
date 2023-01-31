from django.db import models
from localflavor.in_.models import INStateField
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    state = INStateField(null=True,blank=True)

    def __str__(self):
        return str(self.id)