from django.db import models
from django.conf import settings
import random, json

# Create your models here.
class GameLobby(models.Model):
    """
    Databasen indeholder de to spillere som spiller mod hinanden, 
    om spillet er aktivt eller afsluttet
    og hvilke to ord de to spillere skal gætte.
    Resultatet af spillet skal også gemmes
    """
    player_1 = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='player_1')
    player_2 = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='player_2')
    word_1 = models.CharField(max_length=6, name='word_1')
    word_2 = models.CharField(max_length=6, name='word_2')
    
    with open("./words.json", 'r') as f:
        WordList = json.loads(f.read())
    word_1 = WordList['words'][random.randrange(0, len(WordList['words']))]
    word_2 = WordList['words'][random.randrange(0, len(WordList['words']))]
    


class GameInvite(models.Model):
    """
    En spiller skal sende en anden spiller en invitation til at spille. 
    Databasen indeholder en sender, receiver og en boolean om invitationen er accepteret.
    Accepteres invitationen, bliver invitationen inaktiv, og et spil laves.
    """

    sender = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='sender')
    receiver = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='receiver')
    status = models.BooleanField(default=True)

    def accept_invite(self):
        self.status = False
        self.save()
        #Set status to false, and create game_lobby