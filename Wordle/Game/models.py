from django.db import models
from django.conf import settings

# Create your models here.
class GameLobby(models.Model):
    """
    Databasen indeholder de to spillere som spiller mod hinanden, 
    om spillet er aktivt eller afsluttet
    og hvilke to ord de to spillere skal gætte
    """
    player_1 = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='player_1')
    player_2 = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='player_2')
    #word_1 = 
    #word_2 =
    pass

class GameInvite(models.Model):
    """
    En spiller skal sende en anden spiller en invitation til at spille. 
    Databasen indeholder en sender, receiver og en boolean om invitationen er accepteret.
    Accepteres invitationen, bliver invitationen inaktiv, og et spil laves.
    """

    sender = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='sender')
    receiver = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='receiver')
    status = models.BooleanField(default=True)

    def accept(self):
        self.status = False
        self.save()
        #Set status to false, and create game_lobby