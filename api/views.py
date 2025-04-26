from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from .serializer import RegisterSerializer, PhotoSerializer
from user.models import Photos


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'Usuário criado com sucesso'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'detail': 'Credenciais inválidas'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({'detail': 'Logout realizado com sucesso'}, status=status.HTTP_200_OK)


class PhotosView(ViewSet):
    def list(self, request):
        photos = Photos.objects.all()
        serializer = PhotoSerializer(photos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        self.permission_classes = [permissions.IsAuthenticated]
        serializer = PhotoSerializer(data=request.data)
        if not request.user.is_authenticated:
            return Response({'error': 'Você precisa estar logado para criar uma foto'}, status=status.HTTP_401_UNAUTHORIZED)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response({'succes': 'criando com sucesso'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        try:
            photo = Photos.objects.get(pk=pk)
            if photo.author != request.user:
                return Response({'detail': 'Você não tem permissão para deletar esta foto'}, status=status.HTTP_403_FORBIDDEN)
            photo.delete()
            return Response({'detail': 'Foto deletada com sucesso'}, status=status.HTTP_204_NO_CONTENT)
        except Photos.DoesNotExist:
            return Response({'detail': 'Foto não encontrada'}, status=status.HTTP_404_NOT_FOUND)
