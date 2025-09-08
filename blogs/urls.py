from django.urls import path
from .views import (
    BlogListAPIView,
    BlogCreateAPIView,
    BlogDetailAPIView,
    BlogUpdateAPIView,
    BlogDeleteAPIView
)

urlpatterns = [
    # Liste tous les blogs
    path('all/', BlogListAPIView.as_view(), name='blog-list'),

    # Création d'un blog
    path('create/', BlogCreateAPIView.as_view(), name='blog-create'),

    # Détail d'un blog
    path('<int:pk>/', BlogDetailAPIView.as_view(), name='blog-detail'),

    # Mise à jour d'un blog
    path('<int:pk>/update/', BlogUpdateAPIView.as_view(), name='blog-update'),

    # Suppression d'un blog
    path('<int:pk>/delete/', BlogDeleteAPIView.as_view(), name='blog-delete'),
]
