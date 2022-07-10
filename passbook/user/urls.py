from django.urls import include, path
from rest_framework import routers, permissions
from rest_framework.schemas import get_schema_view, openapi

from . import views
from rest_framework.urlpatterns import format_suffix_patterns
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


urlpatterns = [
    #path('', include(router.urls)),
    # path('snippets/', views.SnippetList.as_view()),
    #path('sign-up-1', views.SignUpUser.as_view()),
    path('login', views.Login.as_view()),
    path('sign-up', views.SignUp.as_view()),

    path('user', views.UserList.as_view()),
    #path('user/<int:pk>', views.UserDetail.as_view()),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    #path('profile/', views.UserProfile.as_view(), name='UserProfile'),
    path('profile/<int:pk>', views.UserProfileDetail.as_view(), name='UserProfileDetail'),
    # path('user/<int:pk>/transaction', views.UserTransaction.as_view(), name='Transactions'),   #to create transaction for specific user
    # path('user/<int:pk>/transaction/<int:pk>',views.UserTransaction.as_view(), name='Transactionsdetails'),
]
    #url(r'^$', schema_view),
    # path('swagger-ui/', TemplateView.as_view(
    #     template_name='swagger-ui.html',
    #     extra_context={'schema_url':'openapi-schema'}
    # ), name='swagger-ui'),
    # path('redoc/', TemplateView.as_view(
    #     template_name='redoc.html',
    #     extra_context={'schema_url':'openapi-schema'}
    # ), name='redoc'),


#urlpatterns = format_suffix_patterns(urlpatterns)

