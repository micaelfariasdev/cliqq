from django.urls import path
from . import views

urlpatterns = [
    path('auth/register',
         views.UserView.as_view({'post': 'create'}), name='api-user-register'),
    path('auth/me/',
         views.UserMEViewSet.as_view({'get': 'list'}), name='api-user-me'),
    path('auth/list/',
         views.UserView.as_view({'get': 'list'}), name='api-user-list'),
    path('auth/login/', views.LoginView.as_view(), name='api-login'),
    path('auth/logout/', views.LogoutView.as_view(), name='api-logout'),
    path('photo/upload/',
         views.PhotosView.as_view({'post': 'create'}), name='api-photo-upload'),
    path('photo/delete/<int:pk>/',
         views.PhotosView.as_view({'delete': 'delete'}), name='api-photo-delete'),
    path(
        'photos/', views.PhotosView.as_view({'get': 'list'}), name='api-photos-list'),
    path('photo/view/<str:user>/<int:pk>/',
         views.PhotosViewDetail.as_view(), name='api-photo-detail'),
]
