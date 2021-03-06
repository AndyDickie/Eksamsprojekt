from django.urls import path, include

from . import views


from django.views.generic.base import TemplateView


urlpatterns = [
    path("signup/", views.signup, name='signup'),
    path('login/', views.login_user, name='login'),
    path('add_friend/', views.add_friend, name='add_friend'),
    path('block_user', views.block_user, name='block_user'),
    path("", TemplateView.as_view(template_name='accounts.html'), name='accounts'),
    path('remove_friend/<str:friend_id>', views.remove_friend, name='remove_friend'),
    path('profile/<str:user_id>', views.profile, name='profile'),
    path('leaderboard/<str:leaderboard_type>', views.leaderboard, name='leaderboard'),
    path('leaderboard/', views.leaderboard, name='leaderboard', kwargs={'leaderboard_type': 'global'}),
]