from django.urls import path
from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
    path('gametest/<str:game_id>', views.draw_game, name='gametest'),
    path('challenge/', views.ChallengeFriend, name='challenges'),
    path('accept_invite/<str:friend_id>', views.accept_challenge, name='accept_invite'),
    path('decline_invite/<str:friend_id>', views.decline_challenge, name='decline_invite'),
    path('practice_mode/', views.draw_game_singleplayer, name='singleplayer'),
]