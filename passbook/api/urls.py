from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from . import views
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework_nested import routers

router = SimpleRouter()
router.register('users', views.UserViewSet, basename='users')

transaction_router = routers.NestedSimpleRouter(
    router,
    r'users',
    lookup='user'
)

transaction_router.register(
    r'transactions',
    views.TransactionsViewSet,
    basename='user-transaction'
)

app_name = 'user'

urlpatterns = [
    path('', include(router.urls)),
    path('', include(transaction_router.urls)),
    path('signup', views.SignUp.as_view()),
    path('login', views.Login.as_view(), name='token_obtain_pair'),
    path('login/refresh', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify', jwt_views.TokenVerifyView.as_view(), name='token_verify'),
    # path('profile', views.CreateProfile.as_view()),
    # path('profile/<int:pk>', views.EditProfile.as_view()),
    # path('profile/update/<int:pk>', views.UpdateProfile.as_view()),
    # path('profile/delete/<int:pk>', views.DeleteProfile.as_view()),
    path('transaction', views.TransactionsList.as_view())
]
