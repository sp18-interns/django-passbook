from django.urls import path, include
from django.urls.conf import re_path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('profile', views.ProfileViewSet, basename='profile')
urlpatterns = [
    path('', include(router.urls)),
    path('signup', views.SignUp.as_view()),
    path('login', views.Login.as_view()),
    # path('profile', views.CreateProfile.as_view()),
    # path('profile/<int:pk>', views.EditProfile.as_view()),
    # path('profile/update/<int:pk>', views.UpdateProfile.as_view()),
    # path('profile/delete/<int:pk>', views.DeleteProfile.as_view()),
    path('transaction', views.TransactionsList.as_view())
]
