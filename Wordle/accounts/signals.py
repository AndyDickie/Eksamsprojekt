from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import FriendList, Profile

@receiver(post_save, sender=User)
def create_FriendList(sender, instance, created, **kwargs):
    "creates friendlist to the user that has been created"
    if created:
        FriendList.objects.create(user=instance).save()


@receiver(post_save, sender=User)
def create_FriendList(sender, instance, created, **kwargs):
    "creates Profile model to the user that has been created"
    if created:
        Profile.objects.create(user=instance).save()


        