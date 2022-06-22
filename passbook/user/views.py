from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UserSerializer
from .models import User

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer


# Create your views here.

# class UserViewSet(viewsets.ModelViewSet):
#     """
#     Api endpoints that allows users to be viewed or edited.
#     """
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated]

@api_view(['GET', 'POST'])
def user_list(request, format=None):
    """
    List all code snippets, or create a new user.
    """
    if request.method == 'GET':
        snippets = User.objects.all()
        serializer = UserSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk, format=None):
    """
     Retrieve, update or delete a code
    """
    try:
        user = User.objects.get(pk - pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
