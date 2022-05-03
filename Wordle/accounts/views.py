from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from .forms import Signup
from .models import FriendList
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


def signup(request):
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
    if request.method == 'POST':
        username_ = request.POST.get('name_field')
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
    
    try:
        fl = FriendList.objects.get(user = request.user)
        friends = fl.friends.all()
        print("friends", friends)
        users = User.objects.exclude(username__in = [user.username for user in friends] + [request.user.username])
        print("users", users)
       
    except Exception:
        friends = []
        users = User.objects.exclude(username__in = [user.username for user in friends] + [request.user.username])

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