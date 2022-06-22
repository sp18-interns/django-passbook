from django.urls import include, path
from rest_framework import routers
from . import views


#router = routers.DefaultRouter()
#router.register('users', views.UserViewSet, basename='users')

urlpatterns = [
    #path('', include(router.urls)),
    path('user', views.user_list),
    path('user/<int:pk>', views.user_detail)

]