from django.db import models


# Create your models here.


class User(models.Model):
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=20)

    class Meta:
        ordering = ['email']


class Profile(models.Model):
    name = models.CharField(max_length=100)
    mobile_number = models.BigIntegerField()
    address = models.CharField(max_length=300)
    aadhar_number = models.BigIntegerField()
    pan_number = models.CharField(max_length=10)


