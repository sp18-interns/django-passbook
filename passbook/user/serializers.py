from requests import Response
from rest_framework import serializers, status
from rest_framework.views import APIView

from .models import User, Profile, Transaction, Snippet


class UserSerializer(serializers.ModelSerializer):
    #profiles = serializers.PrimaryKeyRelatedField(many=True, queryset=Profile.objects.all())
    #id = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = User
        fields = ['id', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        Profile.objects.create(user_id=user)
        return user

class ProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Profile
        fields = ['name', 'mobile_number', 'address', 'aadhar_number', 'pan_number', 'user_id']

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']



class TransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['amount', 'transaction_date', 'transaction_type', 'receiver', 'remarks', 'user_id', 'balance']

from rest_framework import serializers



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