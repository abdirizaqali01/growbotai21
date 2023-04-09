from django.urls import path
from .views import index
from . import views

urlpatterns = [
    path('', index),
    path('signup', views.signup, name='signup'),
    path('login', views.login_view, name='login'),
    path('api/chat/', views.chat, name='chat'),
    ]
