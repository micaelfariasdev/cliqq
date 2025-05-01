from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


def new_photo_path(instance, filename):
    return f'photos/{instance.author.username}/{datetime.now().year}/{datetime.now().month}/{datetime.now().day}/{instance.title}.{filename.split(".")[-1]}'

def new_photo_profile_path(instance, filename):
    return f'photos/{instance.user.username}/profile.{filename.split(".")[-1]}'


class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo_perfil = models.ImageField(upload_to=new_photo_profile_path, blank=True, null=True)
    vip = models.BooleanField(blank=True, null=True, default=False)
    biografia = models.TextField(blank=True, null=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    endereco = models.CharField(max_length=255, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.user.username


class Photos(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to=new_photo_path)
    title = models.CharField(max_length=100, blank=False, null=False)
    views = models.IntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    like = models.ManyToManyField(Perfil, related_name='like', blank=True)

    def __str__(self):
        return f"Photo by {self.author.username} on {self.created_at}"
