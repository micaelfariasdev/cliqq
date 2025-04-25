import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Photos

@receiver(post_delete, sender=Photos)
def delete_photo_file(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
