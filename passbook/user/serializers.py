from rest_framework import serializers
from .models import User, Profile, Transaction


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['name', 'mobile_number', 'address', 'aadhar_number', 'pan_number']



class TransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['amount', 'transaction_date', 'transaction_type', 'receiver', 'remarks', 'user_id', 'balance']

