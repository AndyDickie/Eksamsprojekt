from django.dispatch import receiver
from accounts.models import FriendList
from Game.models import GameLobby, GameInvite
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect, render
import json

# Create your views here.

def draw_game(request):
    with open("./words.json", 'r') as f:
        x = json.loads(f.read())
    print("length", len(x['words']))
    print(x['words'][2])
    context = {'word': "glass"}
    return render(request, template_name="game/index.html", context=context)

def ChallengeFriend(request):
    if request.method == 'POST':
        username = request.POST.get('friend_to_challenge')
        GameInvite.objects.create(sender=request.user, receiver=User.objects.get(username=username))

    context = []
    challenges = []
    try:
        fl = FriendList.objects.get(user = request.user)
        friends = fl.friends.all()
        print("friends", friends)
        users = User.objects.exclude(username__in = [user.username for user in friends] + [request.user.username])
        print("users", users)
        

    except Exception:
        friends = []
        users = User.objects.exclude(username__in = [user.username for user in friends] + [request.user.username])
    
    try:
        challenges = GameInvite.objects.filter(receiver = request.user)
        userName_challenge = []
        for challenge in challenges:
            userName_challenge.append(challenge.sender)
        print("ssss", userName_challenge)

    except Exception:    
        userName_challenge = []

    try:
        sent_challenges_objects = GameInvite.objects.filter(sender = request.user)
        sent_challenges = []
        for challenge in sent_challenges_objects:
            sent_challenges.append(challenge.receiver)
        print("ssss", sent_challenges)
        
    except Exception:    
        sent_challenges = []


    context = {
        'users': users,
        'friends': friends,
        'pending_challenges': userName_challenge,
        'sent_challenges': sent_challenges,
    }
    return render(request, 'game/challengeFriend.html', context)

def accept_challenge(request, friend_id):
    invite = GameInvite.objects.get(sender = User.objects.get(username=friend_id), receiver=request.user)
    invite.accept_invite()
    return redirect('test1234')

def decline_challenge(request, friend_id):
    invite = GameInvite.objects.get(sender = User.objects.get(username=friend_id), receiver=request.user)
    invite.decline_invite()
    return redirect('test1234')
