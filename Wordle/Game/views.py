from itertools import chain
from multiprocessing import context
from accounts.models import FriendList
from Game.models import GameLobby, GameInvite, random_word
from django.contrib.auth.models import User
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
        
        game.update_player_result(request.user, int(result))
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
            if GameInvite.objects.get(sender=request.user, receiver=User.objects.get(username=username), active=True): #Does the invite exist?
                error = True  

        except Exception as e:
            if (str(e) == "GameInvite matching query does not exist."):
                GameInvite.objects.create(sender=request.user, receiver=User.objects.get(username=username)) #Create the invite if it doesnt

    #Returns all friends of the user for context
    fl = FriendList.objects.get(user = request.user)
    friends = fl.friends.all()

    #Returns active game invites to the user
    challenges = GameInvite.objects.filter(receiver = request.user)
    userName_challenge = []
    for challenge in challenges:
        if challenge.active is True:
            userName_challenge.append(challenge.sender)

    #Returns sent challenges for context
    sent_challenges_objects = GameInvite.objects.filter(sender = request.user, active=True)
    sent_challenges = []
    for challenge in sent_challenges_objects:
        sent_challenges.append(challenge.receiver)
    
    #CONTEXT HANDLING FOR ACTIVE GAMES
    active_games = list(chain(GameLobby.objects.filter(Player_1=request.user, Player_1_Finished = False, GameFinished = False), GameLobby.objects.filter(Player_2=request.user, Player_2_Finished = False, GameFinished = False)))
    print(active_games)
    game_against = []
    if active_games:
        for game in active_games:
            print("game", game)
            game_against.append(game.playing_against(request.user))

    context = {
            'friends': friends,
            'pending_challenges': userName_challenge,
            'sent_challenges': sent_challenges,
            'error_bool': error,
            'active_games': active_games,
            'game_against': game_against
        }

    return render(request, 'game/GameMenu.html', context)

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

def view_game_details(request, game_id):
    game = GameLobby.objects.get(pk=game_id)
    stats = [[game.Player_1, game.word_1, game.Player_1_Moves, game.Player_2, game.word_2, game.Player_2_Moves, game.get_winner()]]
    
    context = {
        'stats': stats,
    }
    return render(request, 'game/game_details.html', context)