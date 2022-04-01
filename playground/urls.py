from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.say_hello, name='hello'),
    path('login/', views.sut, name='login'),
    path('home/', views.home_screen, name='home'),
    path('', views.redirect_to_home)
]