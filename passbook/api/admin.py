from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Profile, Transactions

UserCredentials = get_user_model()
admin.site.register(UserCredentials)
admin.site.register(Profile)
admin.site.register(Transactions)
