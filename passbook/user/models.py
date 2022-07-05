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
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, null=True)


class Transaction(models.Model):
    class TransactionType(models.TextChoices):
        CREDIT = 'Credit'
        DEBIT = 'Debit'

    amount = models.IntegerField(null=True)
    transaction_date = models.DateTimeField(auto_now=True)
    transaction_type = models.CharField(max_length=6, choices=TransactionType.choices)
    receiver = models.CharField(max_length=200)
    remarks = models.CharField(max_length=200)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    balance = models.IntegerField(null=True)

