from django.contrib.auth.models import User
from rest_framework import serializers
from user.models import Photos, Perfil


class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        fields = ['biografia', 'telefone', 'endereco', 'data_nascimento']
        read_only_fields = ['id', 'user']


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photos
        fields = ['id', 'author', 'image', 'title',
                  'description', 'views', 'created_at']
        read_only_fields = ['id', 'author', 'views', 'created_at']


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
