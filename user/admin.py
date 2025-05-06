from django.contrib import admin
from .models import Photos, Perfil, Story


@admin.register(Photos)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'created_at', 'views']
    search_fields = ['title', 'author__username']
    list_filter = ['created_at', 'author']


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'biografia',
                    'telefone', 'endereco', 'data_nascimento']
    search_fields = ['user']
    list_filter = ['id', 'user']

@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'story_photo',
                    'created_at']
    search_fields = ['author']
    list_filter = ['id', 'author']
