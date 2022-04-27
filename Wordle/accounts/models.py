from django.db import models
from django.conf import settings

# Create your models here.

class FriendList(models.Model):
    #Der er et one to one forhold mellem venneliste og bruger
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user')

    #Vennelisten er many to many, da det indeholder flere users (som venner)
    friends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='friends')

    #Listen over blokerede brugere er et many to many forhold
    blocked_users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='blocked_users')

   
    def add_friend(self, account):
        if not account in self.friends.all():
            self.friends.add(account)
            if account in self.blocked_users.all():
                self.blocked_users.remove(account)
            self.save()

    def remove_friend(self, account):
        if account in self.friends.all():
            self.friends.remove(account)
            self.save()
    
    def block_user(self, account):
        self.blocked_users.add(account)
        if account in self.friends.all():
            self.friends.remove(account)
            self.save()
        pass

    def __str__(self):
        return(self.user.username)


