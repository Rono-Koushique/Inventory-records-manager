from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name='home'),
    path('team', views.team, name='team'),
    path('contacts', views.contacts, name='contacts'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register')
]