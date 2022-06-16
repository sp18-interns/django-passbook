from rest_framework import serializers
from .models import UserCredentials, UserProfile, Transactions

class UserCredentialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCredentials
        fields = ('username','email','password',)
        extra_kwargs = {
            'password': {'write_only': True}
        }

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('name','mobile_number','address','aadhar_number','pan_number',)

class TransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = ('transaction_date','transaction_type','remarks',)
