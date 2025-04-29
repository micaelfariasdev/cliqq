from django.db.models import F
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from .serializer import UserSerializer, PhotoSerializer, PerfilSerializer
from user.models import Photos, Perfil


class UserMEViewSet(ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        user = request.user
        serializer = UserSerializer(user)
        
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserView(ViewSet):
  

    def list(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = UserSerializer(data=request.data)
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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
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


class PhotosViewDetail(APIView):
    def get(self, request, user=None, pk=None):
        try:
            photo = Photos.objects.select_related('author', 'author__perfil').get(author__username=user, pk=pk)
            photo.views += 1
            photo.save(update_fields=['views'])
            serializer = PhotoSerializer(photo)
            return Response(serializer.data, status=200)
        except Photos.DoesNotExist:
            return Response({'detail': 'Foto não encontrada'}, status=404)

class UserViewDetail(APIView):
    def get(self, request, username=None):
        try:
            user = User.objects.filter(username=username).first()
            if not user:
                return Response({'detail': 'Usuário não encontrado'}, status=status.HTTP_404_NOT_FOUND)
            if not user.perfil.photo_perfil:
                photo_url = user.perfil.photo_perfil = 'static/default/image.png'   
                serializer = UserSerializer(user)
                serializer.data['perfil']['photo_perfil'] =  photo_url
                for i in serializer.data['photos']:
                    i['photo_perfil'] = photo_url
                return Response(serializer.data, status=status.HTTP_200_OK)

            
            serializer = UserSerializer(user)


            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'detail': 'Usuário não encontrado'}, status=status.HTTP_404_NOT_FOUND)
