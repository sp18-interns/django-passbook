from django.db import models


# Create your models here.
class Transactions(models.Model):
    class TransactionType(models.TextChoices):
        CREDIT = 'Credit'
        DEBIT = 'Debit'

    transaction_date = models.DateTimeField(auto_now=True)
    transaction_type = models.CharField(max_length=6, choices=TransactionType.choices)
    remarks = models.CharField(max_length=200)
    amount = models.IntegerField(null=True)


class UserProfile(models.Model):
    name = models.CharField(max_length=50)
    mobile_number = models.BigIntegerField()
    address = models.CharField(max_length=300)
    aadhar_number = models.BigIntegerField()
    pan_number = models.TextField()


class UserCredentials(models.Model):
    username = models.CharField(max_length=50)
    password = models.TextField()
    email = models.EmailField()
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, null=True)
    transaction = models.ForeignKey(Transactions, on_delete=models.CASCADE, null=True, )
