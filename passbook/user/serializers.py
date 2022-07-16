from importlib.resources import _

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




class UserSerializer(serializers.ModelSerializer):
    # profiles = serializers.PrimaryKeyRelatedField(many=True, queryset=Profile.objects.all())
    # id = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    # email = serializers.CharField(
    #     max_length=254,
    #     validators=[UniqueValidator(queryset=User.objects.all(),
    #                                 message="Email already exists or already in use")]),

    #confirm_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'confirm_password': {'write_only': True}
        }

        #TODO - CONFIRM PASSWORD/[ENCODED PASSWORD]
        #TODO - TOKEN IMPLEMENTATION

    # def create(self, validated_data):
    #     # user = User.objects.create(validated_data['email'], validated_data['password'])
    #     user = User.objects.create(**validated_data)
    #     Profile.objects.create(user_id=user)
    #     # TODO -> should return a string user login successful
    #     return user

    # def validate(self, data):
    #     if data.get('password') != data.get('confirm_password'):
    #         raise serializers.ValidationError({'Password': 'Password does not match'})
    #     return data

    def validate_email(self, value):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if (re.fullmatch(regex, value)):
            print("Valid Email")
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

    profiles = UserSerializer(many=True, write_only=True)

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
        if len(str(value)) > 12:
            raise serializers.ValidationError('Length of aadhar number is greater than 12')
        elif len(str(value)) < 12:
            raise serializers.ValidationError('Length of aadhar number is smaller than 12')
        else:
            return value

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']

    # def validate(self, data):
    #     email = data.get('email')
    #     password = data.get('password')
    #
    #     if email and password:
    #         user = authenticate(request=self.context.get('request'),
    #                             email=email, password=password)
    #     if not user:
    #         msg = _('Unable to log in with provided credentials.')
    #         raise serializers.ValidationError(msg, code='authorization')
    #     else:
    #         msg = _('Must include "username" and "password".')
    #         raise serializers.ValidationError(msg, code='authorization')
    #
    #     data['user'] = user
    #     return data



class TransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['amount', 'transaction_date', 'transaction_type', 'receiver', 'remarks', 'user_id', 'balance']


