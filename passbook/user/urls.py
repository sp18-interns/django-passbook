from django.urls import include, path
from rest_framework import routers, permissions
from rest_framework.schemas import get_schema_view, openapi


from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView,
)

from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view
from django.views.generic import TemplateView

#router = routers.DefaultRouter()
#router.register('user', views.UserViewSet, basename='users')

# schema_view = get_swagger_view(title='Pastebin API')
from .views import UserTransaction, UserProfile, SignUp, UserDetail, UserProfileDetail, UserTransactionDetail, LoginAPI
from knox import views as knox_views



urlpatterns = [

    path('sign-up', SignUp.as_view(), name='SignUp'),

    path('login', LoginAPI.as_view(), name='login'),
    # path('logout/', knox_views.LogoutView.as_view(), name='logout'),

    # path('user', views.UserList.as_view()),
    path('user/<int:pk>', UserDetail.as_view(), name="User_details"),

    # TODO :- mixing to get the <int:pk>
    path('user/<int:pk>/transaction', UserTransaction.as_view(), name='Transaction'),
    path('user/<int:user_id>/transaction/<int:pk>', UserTransactionDetail.as_view(), name='Transactions_details'),

    # path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # path('profile', views.UserProfile.as_view(), name='UserProfile'),
    path('profile/<int:user_id>', UserProfileDetail.as_view(), name='UserProfileDetail'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


