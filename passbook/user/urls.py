from django.urls import include, path
from rest_framework import routers, permissions
from rest_framework.schemas import get_schema_view, openapi

from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view
from django.views.generic import TemplateView

#router = routers.DefaultRouter()
#router.register('user', views.UserViewSet, basename='users')

# schema_view = get_swagger_view(title='Pastebin API')


urlpatterns = [
    #path('', include(router.urls)),
    path('user', views.UserList.as_view()),
    path('user/<int:pk>', views.UserDetail.as_view()),
    # path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #url(r'^$', schema_view),
    # path('swagger-ui/', TemplateView.as_view(
    #     template_name='swagger-ui.html',
    #     extra_context={'schema_url':'openapi-schema'}
    # ), name='swagger-ui'),
    # path('redoc/', TemplateView.as_view(
    #     template_name='redoc.html',
    #     extra_context={'schema_url':'openapi-schema'}
    # ), name='redoc'),

]

urlpatterns = format_suffix_patterns(urlpatterns)

