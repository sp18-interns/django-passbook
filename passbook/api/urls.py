from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.SignUp.as_view()),
    path('login', views.Login.as_view()),
    path('profile', views.Profile.as_view()),
    path('transaction', views.TransactionsList.as_view())
]