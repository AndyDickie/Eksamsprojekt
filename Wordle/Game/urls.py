from django.urls import path
from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
    path('play/<str:game_id>', views.draw_game, name='play'),
    path('challenge/', views.ChallengeFriend, name='challenges'),
    path('accept_invite/<str:friend_id>', views.accept_challenge, name='accept_invite'),
    path('decline_invite/<str:friend_id>', views.decline_challenge, name='decline_invite'),
    path('practice_mode/', views.draw_game_singleplayer, name='singleplayer'),
    path('view_game_details/<str:game_id>', views.view_game_details, name='game_details')
]