from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Comment
from .serializers import CommentSerializer
from blogs.models import Blog

# ---------------- Liste tous les commentaires d'un blog ----------------
class CommentListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, blog_id):
        comments = Comment.objects.filter(blog_id=blog_id).order_by('-created_at')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


# ---------------- Création d'un commentaire ----------------
class CommentCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, blog_id):
        try:
            blog = Blog.objects.get(pk=blog_id)
        except Blog.DoesNotExist:
            return Response({"detail": "Blog non trouvé"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(author=request.user, blogs=blog)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------------- Détail / Update / Delete d'un commentaire ----------------
class CommentDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            return None

    def get(self, request, pk):
        comment = self.get_object(pk)
        if not comment:
            return Response({"detail": "Commentaire non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def put(self, request, pk):
        comment = self.get_object(pk)
        if not comment:
            return Response({"detail": "Commentaire non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        if comment.author != request.user:
            raise PermissionDenied("Vous n'êtes pas l'auteur de ce commentaire.")
        serializer = CommentSerializer(comment, data=request.data, partial=False, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        comment = self.get_object(pk)
        if not comment:
            return Response({"detail": "Commentaire non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        if comment.author != request.user:
            raise PermissionDenied("Vous n'êtes pas l'auteur de ce commentaire.")
        serializer = CommentSerializer(comment, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        comment = self.get_object(pk)
        if not comment:
            return Response({"detail": "Commentaire non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        if comment.author != request.user:
            raise PermissionDenied("Vous n'êtes pas l'auteur de ce commentaire.")
        comment.delete()
        return Response({"detail": "Commentaire supprimé"}, status=status.HTTP_204_NO_CONTENT)
