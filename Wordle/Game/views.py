from itertools import chain
from accounts.models import FriendList
from Game.models import GameLobby, GameInvite, random_word
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect, render
import json

# Create your views here.
def draw_game_singleplayer(request):
    if request.method == 'POST':
        return redirect('challenges')
    word = random_word()
    context = {'word': word}
    return render(request, template_name="game/index.html", context=context)

def draw_game(request, game_id):
    """
    Renders the game page, and sends the word to guess as context.
    Listents for post method from js, to close the game and awars points
    """
    game = GameLobby.objects.get(pk=game_id)

    #Returner spillerens ord fra game_lobby objektet
    if request.method == 'POST':
        result = request.POST.get('result')
        game.change_player_status(request.user)
        
        game.update_player_result(request.user, result)
        #Try to close the game
        game.end_game()
        print("REUSLT", result)
        return redirect('challenges')
    
    word = game.get_word(request.user)

    context = {'word': word}
    return render(request, template_name="game/index.html", context=context)

def ChallengeFriend(request):
    "Draws the challenge friend page"
    error = False
    challenges = []

    if request.method == 'POST':
        username = request.POST.get('friend_to_challenge')
        try:
            if GameInvite.objects.get(sender=request.user, receiver=User.objects.get(username=username), active=True):
                error = True  

        except Exception as e:
            if (str(e) == "GameInvite matching query does not exist."):
                GameInvite.objects.create(sender=request.user, receiver=User.objects.get(username=username))

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
        print(challenges)
        for challenge in challenges:
            print("llll")
            print("challenge: ", challenge.active)
            if challenge.active == True:
                userName_challenge.append(challenge.sender)
        print("ssss", userName_challenge)

    except Exception:    
        userName_challenge = []

    try:
        sent_challenges_objects = GameInvite.objects.filter(sender = request.user, active=True)
        sent_challenges = []
        for challenge in sent_challenges_objects:
            sent_challenges.append(challenge.receiver)
        print("ssss", sent_challenges)
        
    except Exception:    
        sent_challenges = []

    
    #CONTEXT HANDLING FOR ACTIVE GAMES
    active_games = list(chain(GameLobby.objects.filter(Player_1=request.user, Player_1_Finished = False, GameFinished = False), GameLobby.objects.filter(Player_2=request.user, Player_2_Finished = False, GameFinished = False)))
    print(active_games)
    game_against = []
    if active_games:
        for game in active_games:
            print("game", game)
            game_against.append(game.playing_against(request.user))
    try:
        pass
    except Exception:
        active_games = []
    context = {
            'users': users,
            'friends': friends,
            'pending_challenges': userName_challenge,
            'sent_challenges': sent_challenges,
            'error_bool': error,
            'active_games': active_games,
            'game_against': game_against
        }

    return render(request, 'game/challengeFriend.html', context)

def accept_challenge(request, friend_id):
    "Accept a challenge, and create a game_lobby object"
    invite = GameInvite.objects.get(sender = User.objects.get(username=friend_id), receiver=request.user, active=True)
    invite.accept_invite()
    return redirect('challenges')

def decline_challenge(request, friend_id):
    "Decline a challenge and delete the model object of the friend request"
    invite = GameInvite.objects.get(sender = User.objects.get(username=friend_id), receiver=request.user)
    invite.decline_invite()
    return redirect('challenges')
