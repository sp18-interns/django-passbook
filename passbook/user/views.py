from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.settings import api_settings

from .models import User, Profile, Transaction
from .serializers import SignUpSerializer, ProfileSerializer, TransactionsSerializer, LoginSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework import generics, permissions

from rest_framework_simplejwt.tokens import RefreshToken


class SignUp(generics.GenericAPIView):
    # print(generics.CreateAPIView)
    # queryset = User.objects.all()
    serializer_class = SignUpSerializer

    @swagger_auto_schema(request_body=SignUpSerializer)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        return Response({
            "id": user.id,
            "email": user.email,
            "token": {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
            },
            }, status=status.HTTP_200_OK)


class LoginAPI(generics.GenericAPIView):

    serializer_class = LoginSerializer

    # @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):

        if (request.data.get('email') is None) or (isinstance(request.data['email'], type(None))):
            return Response({'email': 'please provide the email id'}, status=status.HTTP_400_BAD_REQUEST)

        if (request.data.get('password') is None) or (isinstance(request.data['password'], type(None))):
            return Response({'password': 'please provide the password'}, status=status.HTTP_400_BAD_REQUEST)

        else:
            user = User.objects.filter(email=request.data['email'])
            if user:
                if user.values()[0]['password'] == request.data['password']:
                    data = Profile.objects.filter(user_id=list(user)[0].id)
                    # refresh = RefreshToken.for_user(data)
                    return Response({'login': 'login successful.',
                                     # "token": {
                                     #                 'refresh': str(refresh),
                                     #                 'access': str(refresh.access_token),
                                     #     }
                                     }, status=status.HTTP_200_OK)
                else:
                    return Response({'password': "please provide the valid password"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"invalid": "please register with our system"}, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):

    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            profile = Profile.objects.get(user_id=user.id)
            return Response({'email': user.email,
                             'aadhar_number': profile.aadhar_number,
                             'name': profile.name,
                             'address': profile.address,
                             'pan_number': profile.pan_number,
                             'mobile_number': profile.mobile_number,
                             'balance': profile.balance
                             }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"invalid": "user does not exist in the system."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({'invalid': 'wrong input'}, status=status.HTTP_400_BAD_REQUEST)


class UserProfile(APIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    # permission_classes = [permissions.9IsAuthenticated]

    @swagger_auto_schema(request_body=ProfileSerializer)
    def post(self, serializer):
        user = User.objects.get(id=self.request.data['user_id'])
        serializer.save(user_id=user)
        return Response(serializer.data)


class UserProfileDetail(APIView):

    def get_object(self, pk):

        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            print("error")
            pass

    @swagger_auto_schema(request_body=ProfileSerializer)
    def put(self, request, user_id):
        serializer_class = ProfileSerializer()
        profile = Profile.objects.get(user_id=user_id)
        serializer = ProfileSerializer(instance=profile, data=request.data, partial=True)

        # user = self.get_object(user_id)
        # print(user)
        # serializer = ProfileSerializer(user, data=request.data)
        # print(serializer)
        if serializer.is_valid():
            data = serializer.save()
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class UserTransaction(generics.ListCreateAPIView):
#
#     # permission_classes = [permissions.IsAuthenticated]
#     queryset = Transaction.objects.all()                #get and retrieve
#
#     # TODO :- Query profile to get the latest balance
#     # use that take appropriate action (like trying to debit more than balance and all)
#     serializer_class = TransactionsSerializer

# apiview
# pk -> user_id

class UserTransaction(APIView):

    def get_object(self, pk):
        try:
            return Transaction.objects.filter(user_id_id=pk)
        except Transaction.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = TransactionsSerializer(user, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=TransactionsSerializer)
    def post(self, request, pk):
        request.data['user_id'] = pk
        profile = Profile.objects.get(user_id=pk)
        amount = request.data['amount']
        type = request.data['transaction_type']
        if type == 'Credit':
            if amount < 0:
                raise ValueError("invalid amount ")
            profile.balance = profile.balance + amount
        elif request.data['transaction_type'] == 'Debit':
            if amount > profile.balance:
                raise ValueError("insufficient funds")
            profile.balance = profile.balance - amount
        profile.save()
        request.data["closing_balance"] = profile.balance
        serializer = TransactionsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserTransactionDetail(APIView):

    def get_object(self, pk):
        try:
            return Transaction.objects.filter(user_id_id=pk)
        except Transaction.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request,user_id, pk):
        user = Transaction.objects.filter(user_id_id=user_id, pk=pk)
        serializer = TransactionsSerializer(user, many=True)
        return Response(serializer.data)

    # @swagger_auto_schema(request_body=TransactionsSerializer)
    # def put(self, request, user_id, pk):
    #     transaction = self.get_object(pk)
    #     serializer = TransactionsSerializer(transaction, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

