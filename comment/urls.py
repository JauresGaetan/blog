from django.urls import path
from .views import (
    CommentListAPIView,
    CommentCreateAPIView,
    CommentDetailAPIView
)

urlpatterns = [
    # Liste tous les commentaires d'un blog
    path('blog/<int:blog_id>/all/', CommentListAPIView.as_view(), name='comment-list'),

    # Création d'un commentaire pour un blog
    path('blog/<int:blog_id>/create/', CommentCreateAPIView.as_view(), name='comment-create'),

    # Détail / update / delete d'un commentaire
    path('<int:pk>/', CommentDetailAPIView.as_view(), name='comment-detail'),
]
