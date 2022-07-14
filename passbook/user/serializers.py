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

class SignUpSerializer(serializers.ModelSerializer):
    confirm_password = serializers.SerializerMethodField('confirm_password')

    def confirm_password(self, value):
        return value.password == value

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True},
        }


class UserSerializer(serializers.ModelSerializer):
    # profiles = serializers.PrimaryKeyRelatedField(many=True, queryset=Profile.objects.all())
    # id = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    # email = serializers.CharField(
    #     max_length=254,
    #     validators=[UniqueValidator(queryset=User.objects.all(),
    #                                 message="Email already exists or already in use")]),

    class Meta:
        model = User
        fields = ['id', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

        #TODO - CONFIRM PASSWORD/[ENCODED PASSWORD]
        #TODO - TOKEN IMPLEMENTATION

    # def create(self, validated_data):
    #     # user = User.objects.create(validated_data['email'], validated_data['password'])
    #     user = User.objects.create(**validated_data)
    #     Profile.objects.create(user_id=user)
    #     # TODO -> should return a string user login successful
    #     return user

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

    # def validate_confirm_password(self, value):
    #     if User.password == value:
    #         return value
    #     return serializers.ValidationError('Password and confirm password does not match')

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


class TransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['amount', 'transaction_date', 'transaction_type', 'receiver', 'remarks', 'user_id', 'balance']


#from rest_framework import serializers

# class SnippetSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(required=False, allow_blank=True, max_length=100)
#     code = serializers.CharField(style={'base_template': 'textarea.html'})
#     linenos = serializers.BooleanField(required=False)
#
#
#     def create(self, validated_data):
#         """
#         Create and return a new `Snippet` instance, given the validated data.
#         """
#         return Snippet.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Snippet` instance, given the validated data.
#         """
#         instance.title = validated_data.get('title', instance.title)
#         instance.code = validated_data.get('code', instance.code)
#         instance.linenos = validated_data.get('linenos', instance.linenos)
#
#         instance.save()
#         return instance
