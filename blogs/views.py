from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Blog
from .serializers import BlogsSerializers

# ---------------- Liste tous les blogs ----------------
class BlogListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        blogs = Blog.objects.all().order_by('-created_at')
        serializer = BlogsSerializers(blogs, many=True)
        return Response(serializer.data)


# ---------------- Création d'un blog ----------------
class BlogCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = BlogsSerializers(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------------- Détail d'un blog ----------------
class BlogDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Blog.objects.get(pk=pk)
        except Blog.DoesNotExist:
            return None

    def get(self, request, pk):
        blog = self.get_object(pk)
        if not blog:
            return Response({"detail": "Blog non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        serializer = BlogsSerializers(blog)
        return Response(serializer.data)


# ---------------- Mise à jour d'un blog ----------------
class BlogUpdateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Blog.objects.get(pk=pk)
        except Blog.DoesNotExist:
            return None

    def put(self, request, pk):
        blog = self.get_object(pk)
        if not blog:
            return Response({"detail": "Blog non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        if blog.author != request.user:
            raise PermissionDenied("Vous n'êtes pas l'auteur de ce blog.")
        serializer = BlogsSerializers(blog, data=request.data, partial=False, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        blog = self.get_object(pk)
        if not blog:
            return Response({"detail": "Blog non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        if blog.author != request.user:
            raise PermissionDenied("Vous n'êtes pas l'auteur de ce blog.")
        serializer = BlogsSerializers(blog, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------------- Suppression d'un blog ----------------
class BlogDeleteAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Blog.objects.get(pk=pk)
        except Blog.DoesNotExist:
            return None

    def delete(self, request, pk):
        blog = self.get_object(pk)
        if not blog:
            return Response({"detail": "Blog non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        if blog.author != request.user:
            raise PermissionDenied("Vous n'êtes pas l'auteur de ce blog.")
        blog.delete()
        return Response({"detail": "Blog supprimé"}, status=status.HTTP_204_NO_CONTENT)
