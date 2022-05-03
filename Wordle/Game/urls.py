from django.urls import path, include

from . import views


from django.views.generic.base import TemplateView


urlpatterns = [
    path('gametest/', views.draw_game, name='gametest'),
    path('test', views.ChallengeFriend)
]