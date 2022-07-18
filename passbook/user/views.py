from django.shortcuts import render
from knox.models import AuthToken
from knox.serializers import UserSerializer
from rest_framework import viewsets
from rest_framework import permissions

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_202_ACCEPTED, HTTP_401_UNAUTHORIZED, HTTP_200_OK, HTTP_400_BAD_REQUEST, \
    HTTP_404_NOT_FOUND, HTTP_406_NOT_ACCEPTABLE
from rest_framework_simplejwt.settings import api_settings


from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from .models import User, Profile, Transaction
from .serializers import SignUpSerializer, ProfileSerializer, TransactionsSerializer, KnoxUserSerializer, LoginSerializer

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework import mixins
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_swagger.views import get_swagger_view

from .auth import generate_access_token, generate_refresh_token

from django.contrib.auth import login

from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView

# Create your views here.

# class UserViewSet(viewsets.ModelViewSet):
#     """
#     Api endpoints that allows users to be viewed or edited.
#     """
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated]


"""
WRAPPING API VIEWS
"""
# @api_view(['GET', 'POST'])
# def user_list(request, format=None):
#     """
#     List all code snippets, or create a new user.
#     """
#     if request.method == 'GET':
#         snippets = User.objects.all()
#         serializer = UserSerializer(snippets, many=True)
#         return Response(serializer.data)
#
#     elif request.method == 'POST':
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def user_detail(request, pk, format=None):
#     """
#      Retrieve, update or delete a code
#     """
#     try:
#         user = User.objects.get(pk - pk)
#     except User.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         serializer = UserSerializer(user)
#         return Response(serializer.data)
#
#     elif request.method == 'PUT':
#         serializer = UserSerializer(user, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         user.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

"""
CLASS BASED VIEWS
"""

# class UserList(APIView):
#     """
#     List all snippets, or create a new snippet.
#     """
#     def get(self, request, format=None):
#         snippets = User.objects.all()
#         serializer = UserSerializer(snippets, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class UserDetail(APIView):

# def get_object(self, pk):
#     try:
#         return User.objects.get(pk=pk)
#     except User.DoesNotExist:
#         raise Http404
#
# def get(self, request, pk, format=None):
#     snippet = self.get_object(pk)
#     serializer = UserSerializer(snippet)
#     return Response(serializer.data)
#
# def put(self, request, pk, format=None):
#     snippet = self.get_object(pk)
#     serializer = UserSerializer(snippet, data=request.data)
#     if serializer.is_valid():
#         serializer.save(snippet_11)
#         return Response(serializer.data)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# def delete(self, request, pk, format=None):
#     snippet = self.get_object(pk)
#     snippet.delete()
#     return Response(status=status.HTTP_204_NO_CONTENT)

# """
# Using mixins
# """

# class UserList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
# class UserDetail(mixins.RetrieveModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin,
#                     generics.GenericAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

"""
Using generic class-based views
"""


class SignUp(generics.GenericAPIView):
    # print(generics.CreateAPIView)
    # queryset = User.objects.all()
    serializer_class = SignUpSerializer


    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # KnoxUserSerializer.is_valid(raise_exception=True)
        return Response({
            "id": user.id,
            "email": user.email,
            "token": api_settings.TOKEN_OBTAIN_SERIALIZER
        })


class LoginAPI(generics.GenericAPIView):
    # serializer_class = LoginSerializer
    #
    # def post(self, request, *args, **kwargs):
    #     serializer = LoginSerializer(data=request.data, context={'request': request})
    #     serializer.is_valid(raise_exception=True)
    #     user = serializer.validated_data['user']
    #     token, created = Token.objects.get_or_create(user=user)
    #     return Response({"status": status.HTTP_200_OK, "Token": token.key})

    # # permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, format=None, data=None):
        # TODO :- If email is not present then an appropriate message ->Please register with our system - DONE
        # TODO :- Email Present but password wrong - DONE
        # TODO :- By mistake there 2 or email how will you -DONE
        # TODO :- If password is not following the basic strength of password

        if (request.data.get('email') is None) or (isinstance(request.data['email'], type(None))):
            return Response('Please provide the email id', status=status.HTTP_400_BAD_REQUEST)

        if (request.data.get('password') is None) or (isinstance(request.data['password'],type(None))):
            return Response('Please provide the password', status=status.HTTP_400_BAD_REQUEST)

        else:
            user = User.objects.filter(email=request.data['email'])
            if user:
                if user.values()[0]['password'] == request.data['password']:
                    data = Profile.objects.filter(user_id_id=list(user)[0].id)
                    return Response(f'Login successful.', status=status.HTTP_200_OK)
                else:
                    return Response("Please provide the valid password", status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response("Please Register with our system", status=status.HTTP_400_BAD_REQUEST)

# class Login(KnoxLoginView):
#     queryset = User.objects.all()
#     print(queryset)
# serializer_class = UserSerializer
# #
# def perform_create(self, serializer):
#     user = User.objects.get(email=serializer.data["email"])
#     print(user)

# def post(self, request, *args, **kwargs):
#     serializer = User(data=request.data)
#     if serializer.is_valid():
#         # serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# print(repr(UserSerializer()))
# permission_classes = [permissions.IsAuthenticated]

# def post(self, request, *args, **kwargs):
#     serializer_class = UserLoginSerializer(data=request.data)
#     if serializer_class.is_valid(raise_exception=True):
#         return Response(serializer_class.data, status=HTTP_200_OK)
#     return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    # print(repr(UserSerializer()))


# permission_classes = [permissions.IsAuthenticated]


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    print("data")
    queryset = User.objects.all()
    # serializer_class = UserSerializer
    #TODO :- user_id, email,aadhar ,pan ,mobile
    # permission_classes = [permissions.IsAuthenticated]


class UserProfile(generics.ListCreateAPIView):
    #queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    #permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = User.objects.get(id=self.request.data['user_id'])
        serializer.save(user_id=user)
        return Response(serializer.data)

class UserProfileDetail(generics.RetrieveUpdateAPIView):
    #queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    # permission_classes = [permissions.IsAuthenticated]


class UserTransaction(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()

    # TODO :- Query profile to get the latest balance
    # use that take appropriate action (like trying to debit more than balance and all)
    serializer_class = TransactionsSerializer
    # permission_classes = [permissions.IsAuthenticated]

class UserTransactionDetail(generics.RetrieveUpdateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionsSerializer

