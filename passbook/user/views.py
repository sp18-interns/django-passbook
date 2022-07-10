from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, Profile, Transaction
from .serializers import UserSerializer, ProfileSerializer, TransactionsSerializer

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework import mixins
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_swagger.views import get_swagger_view

from .auth import generate_access_token, generate_refresh_token

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

# class SignUpUser(APIView):
#     def post(self, request, format=None):
#         print(request)
#         serializer = UserSerializer.objects.all()
#
#         return Response(UserSerializer.data)


class SignUp(generics.CreateAPIView):
    #print(generics.CreateAPIView)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    #print(repr(UserSerializer()))
    #permission_classes = [permissions.IsAuthenticated]

    # def perform_create(self, serializer):
    #     pass


class Login(generics.CreateAPIView):
    queryset = User.objects.all()
    print(queryset)
    # serializer_class = UserSerializer
    # #
    # def perform_create(self, serializer):
    #     user = User.objects.get(email=serializer.data["email"])
    #     print(user)

    def post(self, request, *args, **kwargs):
        serializer = User(data=request.data)
        if serializer.is_valid():
            # serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # print(repr(UserSerializer()))
    # permission_classes = [permissions.IsAuthenticated]

    # def post(self, request, *args, **kwargs):
    #     serializer_class = UserLoginSerializer(data=request.data)
    #     if serializer_class.is_valid(raise_exception=True):
    #         return Response(serializer_class.data, status=HTTP_200_OK)
    #     return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # print(repr(UserSerializer()))
   # permission_classes = [permissions.IsAuthenticated]


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    #permission_classes = [permissions.IsAuthenticated]


# class UserProfile(generics.ListCreateAPIView):
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer
#     #permission_classes = [permissions.IsAuthenticated]
#
#     def perform_create(self, serializer):
#         user = User.objects.get(id=self.request.data['user_id'])
#         serializer.save(user_id=user)


class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    #permission_classes = [permissions.IsAuthenticated]


class UserTransaction(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionsSerializer
    #permission_classes = [permissions.IsAuthenticated]

# class UserProfile(APIView):
#
#     def post(self, request):
#         serializer = Profile(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def get(self, request):
#         profile = Profile.objects.all()
#         serializer = ProfileSerializer(profile, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def put(self, request, pk):
#         profile = self.get_object(pk)
#         serializer = ProfileSerializer(profile, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk):
#         profile = self.get_object(pk)
#         profile.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# from user.models import Snippet
# from user.serializers import SnippetSerializer
# from django.http import Http404
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
#
#
# class SnippetList(APIView):
#     """
#     List all snippets, or create a new snippet.
#     """
#     def get(self, request, format=None):
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)