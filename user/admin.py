from django.contrib import admin
from .models import Photos, Perfil


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
