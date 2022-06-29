from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.

class UserCredentialsManager(BaseUserManager):
    """
    Defines user creation fields and manages to save user
    """

    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email),
                          username=username,
                          )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_staffuser(self, email, username, password=None):
        user = self.create_user(email,
                                password=password,
                                username=username
                                )
        user.is_staff = True
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(email,
                                password=password,
                                username=username
                                )
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)

        return user


class UserCredentials(AbstractBaseUser):
    """
    Creates a customized database table for user using customized user manager
    """

    # These fields tie to the roles
    class RoleChoice(models.TextChoices):
        ADMIN = 'Admin'
        USER = 'User'

    # ROLE_CHOICES = (
    #     (ADMIN, 'Admin'),
    #     (USER, 'User'),
    # )

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    email = models.EmailField(verbose_name='email address',
                              max_length=255, unique=True,
                              )
    username = models.CharField(verbose_name='username',
                                max_length=150,
                                unique=True,
                                error_messages={
                                    'unique': "A user with that username already exists.",
                                },
                                )
    role = models.CharField(max_length=5, choices=RoleChoice.choices)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]
    objects = UserCredentialsManager()

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


# class User(models.Model):
#     username = models.CharField(max_length=50)
#     password = models.TextField()
#     email = models.EmailField()


class Profile(models.Model):
    name = models.CharField(max_length=50)
    mobile_number = models.BigIntegerField()
    address = models.CharField(max_length=300)
    aadhar_number = models.BigIntegerField()
    pan_number = models.TextField()
    user = models.OneToOneField(UserCredentials, on_delete=models.CASCADE, null=True)


class Transactions(models.Model):
    class TransactionType(models.TextChoices):
        CREDIT = 'Credit'
        DEBIT = 'Debit'

    transaction_date = models.DateTimeField(auto_now=True)
    transaction_type = models.CharField(max_length=6, choices=TransactionType.choices)
    remarks = models.CharField(max_length=200)
    amount = models.IntegerField(null=True)
    user = models.ForeignKey(UserCredentials, on_delete=models.CASCADE, null=True)
