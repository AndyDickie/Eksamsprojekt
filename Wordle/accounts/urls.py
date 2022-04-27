from django.urls import path, include

from . import views

from django.views.generic.base import TemplateView


urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    #path('test/', TemplateView.as_view(template_name='Addfriend.html'),name='addFriendTest'),
    path('test/', views.add_friend, name='add_friend')
]