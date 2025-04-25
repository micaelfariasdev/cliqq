from django.contrib import admin
from .models import Photos


@admin.register(Photos)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'created_at', 'views']
    search_fields = ['title', 'author__username']
    list_filter = ['created_at', 'author']
