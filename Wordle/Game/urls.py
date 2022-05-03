from django.urls import path, include

from . import views


from django.views.generic.base import TemplateView


urlpatterns = [
    path('gametest/', views.draw_game, name='gametest'),
    path('test', views.ChallengeFriend, name='test1234'),
    path('accept_invite/<str:friend_id>', views.accept_challenge, name='accept_invite'),
    path('decline_invite/<str:friend_id>', views.decline_challenge, name='decline_invite'),
]