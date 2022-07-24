

from rest_framework import serializers, status
from rest_framework.validators import UniqueValidator

from .models import User, Profile, Transaction

import re

# User Serializer
# class KnoxUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'email')


class SignUpSerializer(serializers.Serializer):
    # profiles = serializers.PrimaryKeyRelatedField(many=True, queryset=Profile.objects.all())
    # id = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    email = serializers.EmailField(
        max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all(),
                                    message="Email already exists or already in use")])
    password = serializers.CharField()
    confirm_password = serializers.CharField(required=True)

    class Meta:
        fields = ['email', 'password', 'confirm_password']

    def create(self, validated_data):
        data = {'email': validated_data['email'], 'password': validated_data['password']}
        user = User.objects.create(**data)
        Profile.objects.create(user=user)
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


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email']


# class ProfileSerializer(serializers.ModelSerializer):
class ProfileSerializer(serializers.Serializer):
    # user = UserSerializer()

    class Meta:
        # model = Profile
        fields = ['email', 'name', 'mobile_number', 'address', 'aadhar_number', 'pan_number', 'balance']

    def update(self, instance, validated_data, *args, **kwargs):
        # nested_serializer = self.fields['user']
        # nested_instance = instance.user
        # nested_data = validated_data.pop('user')
        user = User.objects.get(pk=instance.pk)
        profile = Profile.objects.get(pk=instance.pk)
        if self.data.serializer.initial_data.get('email'):
            user.email = self.data.serializer.initial_data['email']
            user.save()
        if self.data.serializer.initial_data.get('name'):
            profile.name = self.data.serializer.initial_data['name']
        if self.data.serializer.initial_data.get('pan_number'):
            profile.pan_number = self.data.serializer.initial_data['pan_number']
        profile.save()
        # pro = ProfileSerializer()
        # pro.data['email']

        # nested_serializer.update(nested_instance, nested_data)
        response = {'email': user.email,
                    'aadhar_number': profile.aadhar_number,
                    'name': profile.name,
                    'address': profile.address,
                    'mobile_number': profile.mobile_number,
                    'balance': profile.balance
                    }

        return response

    def validate_mobile_number(self, value):
        if len(str(value)) > 10:
            raise serializers.ValidationError('Length of mobile numbers is greater than 10')
        elif len(str(value)) < 10:
            raise serializers.ValidationError('Length of mobile numbers is smaller than 10')
        else:
            return value

    # def validate_aadhar_number(self, value):
    #     regex = r'/^[01]\d{3}[\s-]?\d{4}[\s-]?\d{4}$/'
    #     if re.fullmatch(regex, value):
    #         return value
    #     else:
    #         raise serializers.ValidationError("Invalid Aadhar number")

    def validate_pan_number(self, value):
        regex = r'[A-Z]{5}[0-9]{4}[A-Z]{1}'
        if re.fullmatch(regex, value):
            return value
        else: raise serializers.ValidationError("Invalid PAN")

    def validate_balance(self, value):
        if value >= 0:
            return value
        else: raise serializers.ValidationError("Please input valid balance")


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

    def create(self, validated_data):
        return Transaction.objects.create(**validated_data)

    # def update(self, instance, validated_data:
    #     instance.amount = validate_data.get('amount', instance.amount))


    def validate_amount(self, value):
        if value > 0
            return value
        else:
            return serializers.ValidationError("Amount should be positive")

    def validate_transaction_type(self, data):
        if ("Credit" or "Debit") in data:
            return data
        else:
            return serializers.ValidationError("Enter Credit or Debit")

    def validate_receiver(self, data):
        if len(data) >= 3:
            return data
        else:
            return serializers.ValidationError("Please provide receiver's name greater than 3 letters")


class Comment(object):
    def __init__(self, email, name, mobile_number, address, aadhar_number, pan_number, balance):
        self.email = email
        self.name = name
        self.mobile_number = mobile_number
        self.address = address
        self.aadhar_number = aadhar_number
        self.pan_number = pan_number
        self.balance = balance

# class CommentSerializer(serializers.Serializer):
#
#
#     email = serializers.EmailField()
#     name = serializers.CharField()
#     mobile_number = serializers.IntegerField()
#     address = serializers.CharField()
#     aadhar_number = serializers.IntegerField()
#     pan_number = serializers.CharField()
#     balance = serializers.IntegerField()
#
#     class Meta:
#
#         fields = ['email', 'mobile_number', 'address', 'aadhar_number', 'pan_number', 'balance']
#
#     def restore_object(self, attrs, instance=None):
#         """
#         Given a dictionary of deserialized field values, either update
#         an existing model instance, or create a new model instance.
#         """
#         if instance is not None:
#             instance.email = attrs.get('email', instance.email)
#             instance.content = attrs.get('name', instance.name)
#             instance.created = attrs.get('mobile_number', instance.mobile_number)
#             instance.content = attrs.get('address', instance.address)
#             instance.created = attrs.get('aadhar_number', instance.aadhar_number)
#             instance.content = attrs.get('pan_number', instance.pan_number)
#             instance.created = attrs.get('balance', instance.balance)
#             return instance
#         return Comment(**attrs)
#
#     def validate_mobile_number(self, value):
#         if len(str(value)) > 10:
#             raise serializers.ValidationError('Length of mobile numbers is greater than 10')
#         elif len(str(value)) < 10:
#             raise serializers.ValidationError('Length of mobile numbers is smaller than 10')
#         else:
#             return value
#
#     def validate_aadhar_number(self, value):
#         regex = r'/^[01]\d{3}[\s-]?\d{4}[\s-]?\d{4}$/'
#         if re.fullmatch(regex, value):
#             return value
#         else:
#             raise serializers.ValidationError("Invalid Aadhar number")
#
#     def validate_pan_number(self, value):
#         regex = r'[A-Z]{5}[0-9]{4}[A-Z]{1}'
#         if re.fullmatch(regex, value):
#             return value
#         else: raise serializers.ValidationError("Invalid PAN")
#
#     def validate_balance(self, value):
#         if value >= 0:
#             return value
#         else: raise serializers.ValidationError("Please input valid balance")
