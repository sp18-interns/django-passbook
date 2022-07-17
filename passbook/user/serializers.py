

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from requests import Response
from rest_framework import serializers, status
from rest_framework.validators import UniqueValidator
from rest_framework.views import APIView
# from django.contrib.auth.models import User

from .models import User, Profile, Transaction

import re

# User Serializer
class KnoxUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')




class SignUpSerializer(serializers.Serializer):
    # profiles = serializers.PrimaryKeyRelatedField(many=True, queryset=Profile.objects.all())
    # id = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    # email = serializers.CharField(
    #     max_length=254,
    #     validators=[UniqueValidator(queryset=User.objects.all(),
    #                                 message="Email already exists or already in use")]),
    email = serializers.EmailField()
    password = serializers.CharField()
    confirm_password = serializers.CharField(required=True)

    class Meta:
        #model = User
        fields = ['email', 'password', 'confirm_password']
        # extra_kwargs = {
        #     'password': {'write_only': True},
        #     'confirm_password': {'write_only': True}
        # }

    # def post_confirm_password(self, data):
    #     if data.get('password') != data.get('confirm_password'):
    #         raise serializers.ValidationError({'Password': 'Password does not match'})
    #     return data

    def create(self, validated_data):
        #user = User.objects.create(validated_data['email'], validated_data['password'], validated_data['confirm_password'])
        data = {'email': validated_data['email'], 'password': validated_data['password']}
        user = User.objects.create(**data)
        Profile.objects.create(user_id=user)
        return user

    def validate(self, data):
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError({'Password': 'Password does not match'})
        return data

    def validate_email(self, value):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if (re.fullmatch(regex, value)):
           # print("Valid Email")
            return value
        else:
            raise serializers.ValidationError("Invalid Email")

    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError('Password is too short!')
        else:
            return value



class ProfileSerializer(serializers.ModelSerializer):
    #user_id = serializers.PrimaryKeyRelatedField(read_only=True)

    profiles = SignUpSerializer(many=True, write_only=True)

    class Meta:
        model = Profile
        fields = ['name', 'mobile_number', 'address', 'aadhar_number', 'pan_number', 'profiles']

    def validate_mobile_number(self, value):
        if len(str(value)) > 10:
            raise serializers.ValidationError('Length of mobile numbers is greater than 10')
        elif len(str(value)) < 10:
            raise serializers.ValidationError('Length of mobile numbers is smaller than 10')
        else:
            return value

    def validate_aadhar_number(self, value):
        regex = r'/^[01]\d{3}[\s-]?\d{4}[\s-]?\d{4}$/'
        if re.fullmatch(regex, value):
            return value
        else:
            raise serializers.ValidationError("Invalid Aadhar number")

    def validate_pan_number(self, value):
        regex = r'[A-Z]{5}[0-9]{4}[A-Z]{1}'
        if re.fullmatch(regex, value):
            return value
        else: raise serializers.ValidationError("Invalid PAN")


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']


class TransactionsSerializer(serializers.Serializer):

    amount = serializers.IntegerField()
    transaction_date = serializers.DateTimeField()
    transaction_type = serializers.CharField()
    receiver = serializers.CharField()
    remarks = serializers.CharField()


    class Meta:
        #model = Transaction
        fields = ['amount', 'transaction_date', 'transaction_type', 'receiver', 'remarks']

    def validate_amount(self, value):
        if value > 0:
            return value
        else:
            return serializers.ValidationError("Amount should be positive")

    def validate_transaction_type(self, data):
        if ("Credit", "Debit") in data:
            return data
        else:
            return serializers.ValidationError("Enter Credit or Debit")

    def validate_receiver(self, data):
        if len(data) >= 3:
            return data
        else:
            return serializers.ValidationError("Please provide receiver's name greater than 3 letters")

