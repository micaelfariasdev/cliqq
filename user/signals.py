import os
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from .models import Photos, Perfil
from django.contrib.auth.models import User
from datetime import datetime


@receiver(post_delete, sender=Photos)
def delete_photo_file(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

@receiver(pre_save, sender=Perfil)
def delete_photo_file(sender, instance, **kwargs):
    if instance.photo_perfil:
        if os.path.isfile(instance.photo_perfil.path):
            os.remove(instance.photo_perfil.path)

@receiver(post_delete, sender=Perfil)
def delete_photo_file(sender, instance, **kwargs):
    if instance.photo_perfil:
        if os.path.isfile(instance.photo_perfil.path):
            os.remove(instance.photo_perfil.path)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)
