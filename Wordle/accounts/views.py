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
            fl.add_friend(friend_user)
            fl.save()
              
        except Exception: 
            fl = FriendList.objects.create(user = user)
            fl.add_friend(friend_user)
            fl.save()
    
    
    
    try:
        fl = FriendList.objects.get(user = request.user)
        friends = fl.friends.all()
        print("friends", friends)
        # exclude user from users in friends

        users = User.objects.exclude(username__in = [user.username for user in friends] + [request.user.username])
        print("users", users)
       
    except Exception:
        users = User.objects.all()
        friends = None
    
    #users.remove(request.user)

    context = {
        'users': users,
        'friends': friends
    }
        
    return render(request, "Addfriend.html", context)