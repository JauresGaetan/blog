from rest_framework import serializers
from .models import Blog

class BlogsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'image', 'created_at', 'author']
        read_only_fields = ['author', 'created_at']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['author'] = request.user
        return super().create(validated_data)