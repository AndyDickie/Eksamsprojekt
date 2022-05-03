from accounts.models import FriendList
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
import json

# Create your views here.

def draw_game(request):
    with open("./words.json", 'r') as f:
        x = json.loads(f.read())
    print("length", len(x['words']))
    print(x['words'][2])
    return render(request, template_name="game/index.html")

def ChallengeFriend(request):
    context = []
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
    return render(request, 'game/challengeFriend.html', context)