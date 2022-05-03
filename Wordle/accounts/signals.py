from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import FriendList

@receiver(post_save, sender=User)
def create_FriendList(sender, instance, created, **kwargs):
    if created:
        FriendList.objects.create(user=instance).save()
  
# @receiver(post_save, sender=User)
# def save_profile(sender, instance, **kwargs):
#         instance.friendlist.save()
        