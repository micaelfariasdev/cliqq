import os
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from .models import Photos, Perfil, Story
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from PIL import Image


@receiver(post_delete, sender=Photos)
def delete_photo_file(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

@receiver(post_save, sender=Photos)
def delete_photo_file(sender, instance, **kwargs):
    if sender.image:
        img = Image.open(instance.image.path)
        if img.size[0] or img.size[1] > 1080:
            img = img.resize((1080, 1080))
        img = img.convert('RGBA')
        fundo_branco = Image.new('RGB', img.size, (255, 255, 255))
        fundo_branco.paste(img, mask=img.split()[3])
        fundo_branco.save(instance.image.path, quality=85, format='JPEG')
        img.close()
        fundo_branco.close()

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

@receiver(post_delete, sender=Story)
def delete_story_file(sender, instance, **kwargs):
    if instance.story_photo:
        if os.path.isfile(instance.story_photo.path):
            os.remove(instance.story_photo.path)