from django.urls import include, path
from rest_framework import routers
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

#router = routers.DefaultRouter()
#router.register('user', views.UserViewSet, basename='users')

urlpatterns = [
    #path('', include(router.urls)),
    path('user', views.UserList.as_view()),
    path('user/<int:pk>', views.UserDetail.as_view())

]

urlpatterns = format_suffix_patterns(urlpatterns)

