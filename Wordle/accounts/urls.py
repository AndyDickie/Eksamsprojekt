from django.urls import path, include

from . import views


from django.views.generic.base import TemplateView


urlpatterns = [
    path("signup/", views.signup, name='signup'),
    path('login/', views.login_user, name='login'),
    path('test/', views.add_friend, name='add_friend'),
    path('block_user', views.block_user, name='block_user'),
    path('gametest/', TemplateView.as_view(template_name='game/index.html'), name='gametest')
]