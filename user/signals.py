import os
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from .models import Photos, Perfil
from django.contrib.auth.models import User



@receiver(post_delete, sender=Photos)
def delete_photo_file(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)
