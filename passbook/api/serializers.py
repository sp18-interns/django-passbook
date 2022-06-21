from rest_framework import serializers
from .models import User, Profile, Transactions


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)
        extra_kwargs = {
            'password': {'write_only': True}
        }


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('user', 'name', 'mobile_number', 'address', 'aadhar_number', 'pan_number',)

class TransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = ('user', 'transaction_date', 'transaction_type', 'amount', 'remarks',)
