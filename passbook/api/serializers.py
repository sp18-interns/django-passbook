from abc import ABC

from rest_framework import serializers
from .models import UserCredentials, Profile, Transactions
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['role'] = user.role
        return token


class SignupSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new user using signup form
    """

    class Meta:
        model = UserCredentials
        fields = ['id', 'username', 'email', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        if validate_password(validated_data['password']) is None:
            password = make_password(validated_data['password'])
            user = UserCredentials.objects.create(
                username=validated_data['username'],
                email=validated_data['email'],
                password=password,
                role=validated_data['role']
            )
            return user


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password',)
#         extra_kwargs = {
#             'password': {'write_only': True}
#         }
#

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('user', 'name', 'mobile_number', 'address', 'aadhar_number', 'pan_number',)


class TransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = ('user', 'transaction_date', 'transaction_type', 'amount', 'remarks',)
