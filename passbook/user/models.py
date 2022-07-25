from django.db import models


class User(models.Model):
    id = models.AutoField(
        primary_key=True)  # AutoField is an IntegerField that automatically increments according to available IDs
    email = models.EmailField(unique=True,
                              max_length=254)  # EmailField is a CharField that checks the value for a valid email address using EmailValidator.
    password = models.CharField(max_length=20)  # CharField is a string field, for small- to large-sized strings


class Profile(models.Model):
    name = models.CharField(max_length=100)
    mobile_number = models.BigIntegerField(null=True)
    address = models.CharField(max_length=300)
    aadhar_number = models.BigIntegerField(null=True)
    pan_number = models.CharField(max_length=10)
    balance = models.IntegerField(null=True)
    user = models.OneToOneField(User, related_name='User', on_delete=models.CASCADE, primary_key=True)


class Transaction(models.Model):
    class TransactionType(models.TextChoices):
        CREDIT = 'Credit'
        DEBIT = 'Debit'

    amount = models.IntegerField()
    transaction_date = models.DateTimeField(auto_now=True)
    transaction_type = models.CharField(max_length=6, choices=TransactionType.choices)
    receiver = models.CharField(max_length=200)
    remarks = models.CharField(max_length=200)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions")
    closing_balance = models.IntegerField(null=True)
