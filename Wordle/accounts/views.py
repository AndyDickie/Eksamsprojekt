from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.models import User

from .models import FriendList
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

@login_required 
def add_friend(request):
    if request.method == 'POST':
        username_ = request.POST.get('name_field')
        friend_user = User.objects.get(username = username_)
        user = request.user
        
        try:
            fl = FriendList.objects.get(user = user)

        except Exception:
            fl = FriendList.objects.create(user = user)
        
        try:
            other_fl = FriendList.objects.get(user = friend_user)
        
        except Exception:
            other_fl = FriendList.objects.create(user = friend_user)

        if not user in other_fl.blocked_users.all():
            fl.add_friend(friend_user)
            other_fl.add_friend(user)
            fl.save()

        if user in other_fl.blocked_users.all():
            raise ValueError("The user has blocked you")
    
    try:
        fl = FriendList.objects.get(user = request.user)
        friends = fl.friends.all()
        print("friends", friends)
        users = User.objects.exclude(username__in = [user.username for user in friends] + [request.user.username])
        print("users", users)
       
    except Exception:
        users = User.objects.exclude(username__in = [user.username for user in friends] + [request.user.username])
        friends = None

    context = {
        'users': users,
        'friends': friends
    }

    return render(request, "Addfriend.html", context)

@login_required
def block_user(request):
    if request.method == 'POST':
        username_ = request.POST.get('name_field')
        blocked_user = User.objects.get(username = username_)
        user = request.user

        try:
            fl = FriendList.objects.get(user = user)

        except Exception: 
            fl = FriendList.objects.create(user = user)
        
        fl.block_user(blocked_user)
        
        try:
            other_fl = FriendList.objects.get(user = blocked_user)
        
        except Exception:
            other_fl = FriendList.objects.create(user = blocked_user)

        other_fl.remove_friend(user)

    user = request.user
    friends = FriendList.objects.get(user = request.user).friends.all()
    users = User.objects.exclude(username__in = [request.user.username])
    
    context = {
        'users': users,
        'friends': friends
    }

    return render(request, "blockFriend.html", context)