from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile
from django.contrib.auth.models import User

@receiver(post_save,sender=User)
def CreateProfile(sender,**kwargs):
    if kwargs["created"]:
        Profile.objects.create(user=kwargs["instance"])