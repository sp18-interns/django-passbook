from django.db import models


# Create your models here.


class User(models.Model):
    id = models.AutoField(primary_key=True)                 #AutoField is an IntegerField that automatically increments according to available IDs
    email = models.EmailField(unique=True, max_length=254)  #EmailField is a CharField that checks the value for a valid email address using EmailValidator.
    password = models.CharField(max_length=20)              #CharField is a string field, for small- to large-sized strings

    class Meta:
        ordering = ['email']


class Profile(models.Model):

    name = models.CharField(max_length=100, null=True)
    mobile_number = models.BigIntegerField(null=True)
    address = models.CharField(max_length=300, null=True)
    aadhar_number = models.BigIntegerField(null=True)
    pan_number = models.CharField(max_length=10,null=True)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profiles')


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






# class Snippet(models.Model):
#     created = models.DateTimeField(auto_now_add=True)
#     title = models.CharField(max_length=100, blank=True, default='')
#     code = models.TextField()
#     linenos = models.BooleanField(default=False)
#
#
#     class Meta:
#         ordering = ['created']

