from django.contrib.auth.models import User
from rest_framework import serializers
from user.models import Photos, Perfil
from .utils import humanize_time_difference


class PerfilSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='user', read_only=True)

    class Meta:
        model = Perfil
        fields = ['author', 'biografia', 'telefone',
                  'endereco', 'data_nascimento', 'photo_perfil']
        read_only_fields = ['id', 'author']


class PhotoSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)
    photo_perfil = serializers.CharField(source='author.perfil.photo_perfil.url', read_only=True)
    post_hour = serializers.SerializerMethodField()

    class Meta:
        model = Photos
        fields = ['id', 'photo_perfil', 'author', 'image', 'title',
                  'description', 'views', 'created_at', 'post_hour']
        read_only_fields = ['id', 'photo_perfil', 'author',
                            'views', 'created_at', 'post_hour']
        

    def get_post_hour(self, obj):
        return humanize_time_difference(obj.created_at)




class UserSerializer(serializers.ModelSerializer):
    perfil = PerfilSerializer(required=False)
    password = serializers.CharField(write_only=True)
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name',
                  'last_name', 'email', 'password', 'perfil', 'photos']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user
