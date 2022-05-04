from django.db import models
from django.conf import settings
import random, json

def random_word():
    with open("./words.json", 'r') as f:
        WordList = json.loads(f.read())
    return WordList['words'][random.randrange(0, len(WordList['words']))]

# Create your models here.
class GameLobby(models.Model):
    """
    Databasen indeholder de to spillere som spiller mod hinanden, 
    om spillet er aktivt eller afsluttet
    og hvilke to ord de to spillere skal gætte.
    Resultatet af spillet skal også gemmes
    """
    Player_1 = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='player_1')
    Player_2 = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='player_2')

    Word_1 = models.CharField(max_length=5, name='word_1', default=random_word)
    Word_2 = models.CharField(max_length=5, name='word_2', default=random_word)

    GameStatus = models.BooleanField(default=True)

    Player_1_Status = models.BooleanField(default=False)
    Player_2_Status = models.BooleanField(default=False)

    #moves to win?
    

    def get_word(self, account):
        if account in self.Player_1.all():
            return self.Word_1
        if account in self.Player_2.all():
            return self.Word_2
        else:
            return None
    
    def change_player_status(self, account):
        if account in self.Player_1.all():
            self.Player_1_Status = True
            self.save()
        if account in self.Player_2.all():
            self.Player_2_Status = True
            self.save()
        else:
            return
    
    def end_game(self):
        pass

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

    def accept_invite(self):
        #Set status to false, and create game_lobby
        print("ACCEPTED")
        self.delete()

        
    def decline_invite(self):
        print("DELETED")
        self.delete()