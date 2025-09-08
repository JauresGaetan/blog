from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    author_firstname = serializers.CharField(source='user.firstname', read_only=True)  # ← ajouté

    class Meta:
        model = Comment
        fields = ['id', 'blog', 'user', 'author_firstname', 'message', 'created_at']
        read_only_fields = ['user', 'author_firstname', 'created_at']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user
        return super().create(validated_data)