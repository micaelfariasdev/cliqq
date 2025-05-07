from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from user.models import Photos, Perfil, Story
from .utils import humanize_time_difference
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta

class StorySerializer(serializers.ModelSerializer):
    post_hour = serializers.SerializerMethodField()
    active = serializers.SerializerMethodField()

    class Meta:
        model = Story
        fields = '__all__'
        
    def get_post_hour(self, obj):
        return humanize_time_difference(obj.created_at)
    
    def get_active(self, obj):
        now = datetime.now(obj.created_at.tzinfo)
        return (now - obj.created_at) < timedelta(hours=24)

class PerfilSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='user', read_only=True)

    class Meta:
        model = Perfil
        fields = ['id','author', 'biografia', 'telefone',
                  'endereco', 'data_nascimento', 'photo_perfil', 'vip']
        read_only_fields = ['id', 'author', 'vip']


class PhotoSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)
    photo_perfil = serializers.SerializerMethodField()
    post_hour = serializers.SerializerMethodField()

    class Meta:
        model = Photos
        fields = ['id', 'photo_perfil', 'author', 'image', 'title',
                  'description', 'views', 'created_at', 'post_hour', 'like']
        read_only_fields = ['id', 'photo_perfil', 'author',
                            'views', 'created_at', 'post_hour', 'like'] 
        

    def get_post_hour(self, obj):
        return humanize_time_difference(obj.created_at)
    
    def get_photo_perfil(self, obj):
        perfil = obj.author.perfil
        if perfil.photo_perfil and hasattr(perfil.photo_perfil, 'url'):
            return perfil.photo_perfil.url
        return '/static/default/image.png'




class UserSerializer(serializers.ModelSerializer):
    perfil = PerfilSerializer(required=False)
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    photos = PhotoSerializer(many=True, read_only=True)
    username = serializers.CharField(
        max_length=150, required=True, allow_blank=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password', 'perfil', 'photos']
        extra_kwargs = {
            'email': {'required': True},
        }

    def validate(self, data):
        import re
        data = super().validate(data)
        errors = {}

        password = data.get('password')
        password_errors = []

        username = data.get('username').lower()
        username_errors = []

        if len(password) < 8:
            password_errors.append('A senha deve ter no mínimo 8 caracteres.')
        if not re.search(r'\d', password):
            password_errors.append('A senha deve conter pelo menos um número.')
        if not re.search(r'[a-z]', password):
            password_errors.append('A senha deve conter pelo menos uma letra minúscula.')
        if not re.search(r'[A-Z]', password):
            password_errors.append('A senha deve conter pelo menos uma letra maiúscula.')
        if not re.search(r'[!@#$%^&*()_+\-=\[\]{};\'\\:"|<,./<>?]', password):
            password_errors.append('A senha deve conter pelo menos um caractere especial.')

        if password_errors:
            errors['password'] = password_errors

        if data.get('password') != data.get('confirm_password'):
            errors['confirm_password'] = 'As senhas não coincidem.'

        try:
            if User.objects.filter(username=username).exists():
                username_errors.append('Nome de usuário já está em uso.')
            if len(username) < 8:
                username_errors.append('Nome de usuário deve ter no mínimo 5 caracteres.')
        except ValidationError as e:
            username_errors.append(str(e))

        if username_errors:
            errors['username'] = username_errors
        try:
            if User.objects.filter(email=data.get('email')).exists():
                errors['email'] = 'Este e-mail já está cadastrado.'
        except ValidationError as e:
            errors['email'] = str(e)

        if errors:
            raise serializers.ValidationError(errors)
        
        print(data)
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user

    

    


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user is None:
            raise serializers.ValidationError({'non_field_errors': ['Credenciais inválidas.']})
        data['user'] = user
        return data
