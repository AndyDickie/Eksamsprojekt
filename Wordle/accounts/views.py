from email import iterators
import re
from django.shortcuts import render, redirect
from itertools import chain
from django.contrib.auth.models import User
from .forms import Signup
from .models import FriendList, Profile
from Game.models import GameInvite, GameLobby
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import itertools


def signup(request):
    "signup"
    form = Signup()
    context = {
        'form': form,
        'error': [],
        'error_bool': False,
    }
    if request.method == 'POST':
        form = Signup(request.POST)
        if form.is_valid():
            # Save user to database
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            if username and email and password:
                user = User.objects.create_user(
                    username=form.cleaned_data['username'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password']
                )
                user.save()

                # Login
                login(request, user)

                # Redirect
                return redirect('home')

            if not username:
                context['error'].append("Username is missing!")
            if not email:
                context['error'].append("Email is missing!")
            if not password:
                context['error'].append("Password is missing!")
            
            if context['error']:
                context['error_bool'] = True
            
    return render(request, 'registration/signup.html', context)


def login_user(request):
    "login_user"
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            print("Login!!!")
            login(request, user)
            return redirect("home")
        else:
            return render(request, "registration/login.html", context = {'error_bool': True, 'error': 'User not found'})
    return render(request, "registration/login.html")


@login_required 
def add_friend(request):
    "add_friend"
    if request.method == 'POST':
        username_ = request.POST.get('friend_name')
        print(username_)
        friend_user = User.objects.get(username = username_)
        user = request.user
        
        fl = FriendList.objects.get(user = user)
        other_fl = FriendList.objects.get(user = friend_user)
        
        if not user in other_fl.blocked_users.all():
            fl.add_friend(friend_user)
            other_fl.add_friend(user)
            fl.save()

        if user in other_fl.blocked_users.all():
            raise ValueError("The user has blocked you")
    
    fl = FriendList.objects.get(user = request.user)
    friends = fl.friends.all()
    users = User.objects.exclude(username__in = [user.username for user in friends] + [request.user.username])
       
    context = {
        'users': users,
        'friends': friends
    }

    return render(request, "Addfriend.html", context)

@login_required
def block_user(request):
    "block_user"
    if request.method == 'POST':
        username_ = request.POST.get('name_field')
        blocked_user = User.objects.get(username = username_)
        user = request.user

        fl = FriendList.objects.get(user = user)
        fl.block_user(blocked_user)

        other_fl = FriendList.objects.get(user = blocked_user)
        other_fl.remove_friend(user)

    user = request.user
    friends = FriendList.objects.get(user = request.user).friends.all()
    users = User.objects.exclude(username__in = [request.user.username])
    
    context = {
        'users': users,
        'friends': friends
    }

    return render(request, "blockFriend.html", context)

@login_required
def remove_friend(request, friend_id):
    "remove_friend"
     
    fl = FriendList.objects.get(user = request.user)
    other_fl = FriendList.objects.get(user = friend_to_remove)

    friend_to_remove = User.objects.get(username = friend_id)
    
    fl.remove_friend(friend_to_remove)
    other_fl.remove_friend(request.user)
    print(friend_id)
    return redirect('add_friend')

@login_required
def profile(request, user_id):
    user = User.objects.get(pk = user_id)
    bool = False

    completed_games = list(chain(GameLobby.objects.filter(Player_1=user, GameFinished = True), GameLobby.objects.filter(Player_2=user, GameFinished = True)))[:10]
    game_status = [[game.playing_against(user), game.get_winner(), game.id] for game in completed_games]
    
    #Returns the game where the user has finished the game, but is waiting for the opponent
    pending_games = list(chain(GameLobby.objects.filter(Player_1=user, Player_1_Finished = True, GameFinished = False, Player_2_Finished = False), GameLobby.objects.filter(Player_2=user, Player_2_Finished = True, GameFinished = False, Player_1_Finished = False)))
    pending_games = [game.playing_against(user) for game in pending_games]
    print("pending games", pending_games)
    if pending_games:
        bool = True
    
    user_results = Profile.objects.get(user=user)
    #Sent as list of list for easy unpacking in html
    stats = [[user_results.wins, user_results.draws, user_results.losses, user_results.av_moves, user_results.total_games]] 

    context = {
        'game_status': game_status,
        'pending': pending_games,
        'stats': stats,
        'bool': bool
    }
    return render(request, 'profile.html', context)

def leaderboard(request, leaderboard_type="global"):
    if leaderboard_type == "friends":
        user = request.user
        friends = FriendList.objects.get(user=user).friends.all()
        profiles = Profile.objects.filter(user__in = friends)
        user_profile = Profile.objects.filter(user=request.user)
        profiles = profiles.union(user_profile).order_by('-wins')[:50]
        counter = itertools.count(1)
        stats = [[user.wins, user.draws, user.losses, user, next(counter), user.av_moves, user.total_games] for user in profiles]
        type = "Friends"
        
    elif leaderboard_type == "global":
        counter = itertools.count(1)
        profiles = Profile.objects.all().order_by('-wins')[:50]
        stats = [[user.wins, user.draws, user.losses, user, next(counter), user.av_moves, user.total_games] for user in profiles]
        type = "Global"
    
    context = {
        'profiles': profiles,
        'stats': stats,
        'type': type
        }
    return render(request, 'leaderboard.html', context)