from rest_framework import serializers
from .models import BlogsComment

class BlogsCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogsComment
        fields = '__all__'
  
