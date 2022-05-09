from django.db import models
from django.conf import settings
import random, json
from accounts.models import Profile

def random_word():
    "Returns a random word from the json file"
    with open("./words.json", 'r') as f:
        WordList = json.loads(f.read())
    return WordList['words'][random.randrange(0, len(WordList['words']))]

class GameInvite(models.Model):
    """
    En spiller skal sende en anden spiller en invitation til at spille. 
    Databasen indeholder en sender, receiver og en boolean om invitationen er accepteret.
    Accepteres invitationen, bliver invitationen inaktiv, og et spil laves.
    """

    #sender = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='sender')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name='sender', on_delete=models.CASCADE)
    #receiver = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='receiver')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name='receiver', on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def accept_invite(self):
        "accepts invite, and creates a instance og game_lobby object"
        self.active = False
        self.save()
        print("SSSSSSS", self.sender, self.receiver, self)
        game = GameLobby(Player_1 = self.sender, Player_2 = self.receiver, game_invite = self)
        game.save()
        print("ACCEPTED")

        
    def decline_invite(self):
        "declines invite and deletes instance of invite"
        print("DELETED")
        self.delete()

    def __str__(self):
        return (f"sender:{self.sender} receiver:{self.receiver}")

# Create your models here.
class GameLobby(models.Model):
    """
    Databasen indeholder de to spillere som spiller mod hinanden, 
    om spillet er aktivt eller afsluttet
    og hvilke to ord de to spillere skal gætte.
    Resultatet af spillet skal også gemmes
    """
    Player_1 = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name='player_1', on_delete=models.CASCADE, blank=True)
    Player_2 = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name='player_2', on_delete=models.CASCADE, blank=True)

    game_invite = models.ForeignKey(GameInvite, name='game_invite', on_delete=models.CASCADE, null=True, blank=True)

    Word_1 = models.CharField(max_length=5, name='word_1', default=random_word)
    Word_2 = models.CharField(max_length=5, name='word_2', default=random_word)

    GameFinished = models.BooleanField(default=False, name="GameFinished")

    Player_1_Finished = models.BooleanField(default=False) #True means finished
    Player_2_Finished = models.BooleanField(default=False)

    Player_1_Moves = models.IntegerField(blank=True, name='Player_1_Moves', default=6)
    Player_2_Moves = models.IntegerField(blank=True, name='Player_2_Moves', default=6)

    def __str__(self):
        return (f"Game Lobby: {self.game_invite}")

    def get_word(self, account):
        "Returns the word belonging to the account"
        if account == self.Player_1:
            return str(self.word_1)

        if account == self.Player_2:
            return str(self.word_2)
    
    def change_player_status(self, account):
        "changes player_status for account to finished"
        if account == self.Player_1:
            self.Player_1_Finished = True
            self.save()
        if account == self.Player_2:
            self.Player_2_Finished = True
            self.save()
        else:
            return
    
    def update_player_result(self, account, result):
        if account == self.Player_1:
            self.Player_1_Moves = result
            self.save()
        if account == self.Player_2:
            self.Player_2_Moves = result
            self.save()

    def playing_against(self, account):
        if account == self.Player_1:
            return f"Game against {self.Player_2.username}"
        if account == self.Player_2:
            return f"Game against {self.Player_1.username}"
    
    def get_winner(self):
        "returns the winner user, or draw"
        print(self.Player_1_Moves, self.Player_2_Moves)
        print(type(self.Player_1_Moves), type(self.Player_2_Moves))
        if self.GameFinished == True:
            if self.Player_1_Moves == self.Player_2_Moves:
                return "draw"
            if self.Player_1_Moves < self.Player_2_Moves:
                return self.Player_1
            if self.Player_2_Moves < self.Player_1_Moves:
                return self.Player_2

    def add_points(self, account):
        user_profile = Profile.objects.get(user=account)
        result = self.get_winner()
        if result == "draw":
            user_profile.add_draw()

        elif result == account:
            user_profile.add_win()
        
        else:
            user_profile.add_loss()
        


    def end_game(self):
        "set the game status to finished"
        print("player 1 og 2 status:", self.Player_1_Finished, self.Player_2_Finished)
        if self.Player_1_Finished == True and self.Player_2_Finished == True:
            self.GameFinished = True
            self.add_points(account=self.Player_1)
            self.add_points(account=self.Player_2)
            self.save()

    
