from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics, mixins, permissions, viewsets
from .models import UserCredentials, UserProfile, Transactions
from .serializers import UserProfileSerializer, UserCredentialsSerializer, TransactionsSerializer


# Create your views here.

# class MultipleFieldLookupMixin:
#     """
#     Apply this mixin to any view or viewset to get multiple field filtering
#     based on a `lookup_fields` attribute, instead of the default single field filtering.
#     """
#
#     def get_object(self):
#         queryset = self.get_queryset()  # Get the base queryset
#         queryset = self.filter_queryset(queryset)  # Apply any filter backends
#         filter = {}
#         for field in self.lookup_fields:
#             if self.kwargs[field]:  # Ignore empty fields.
#                 filter[field] = self.kwargs[field]
#         obj = get_object_or_404(queryset, **filter)  # Lookup the object
#         self.check_object_permissions(self.request, obj)
#         return obj


class SignUp(generics.CreateAPIView):
    # def post(self, request):
    #     serializer = UserCredentialsSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    queryset = UserCredentials.objects.all()
    serializer_class = UserCredentialsSerializer


class Login(generics.CreateAPIView):
    # def post(self, request):
    #     serializer = UserCredentialsSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    queryset = UserCredentials.objects.all()
    serializer_class = UserCredentialsSerializer


# class Profile(APIView):
#
#     def post(self, request):
#         serializer = UserProfileSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def get(self, request):
#         profile = UserProfile.objects.all()
#         serializer = UserProfileSerializer(profile, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def put(self, request, pk):
#         profile = self.get_object(pk)
#         serializer = UserProfileSerializer(profile, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk):
#         profile = self.get_object(pk)
#         profile.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
class CreateProfile(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class EditProfile(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UpdateProfile(generics.UpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class DeleteProfile(generics.DestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()



class TransactionsViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin):
    serializer_class = TransactionsSerializer
    queryset = Transactions.objects.all()

class TransactionsList(APIView):
    def post(self, request):
        serializer = TransactionsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        transaction = Transactions.objects.all()
        serializer = TransactionsSerializer(transaction, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        transaction = self.get_object(pk)
        serializer = TransactionsSerializer(transaction, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        transaction = self.get_object(pk)
        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
