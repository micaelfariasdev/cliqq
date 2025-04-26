from django.contrib.auth.models import User
from rest_framework import serializers
from user.models import Photos


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photos
        fields = ['id', 'author', 'image', 'title', 'description', 'views', 'created_at']
        read_only_fields = ['id', 'author', 'views', 'created_at']
