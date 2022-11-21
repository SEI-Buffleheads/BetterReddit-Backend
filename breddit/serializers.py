from .models import Post, Comment
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class PostSerializer(serializers.ModelSerializer):
  class Meta:
    model = Post
    fields = '__all__'
    owner = serializers.ReadOnlyField(source='owner.username')
    
class CommentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Comment
    fields = '__all__'
    owner = serializers.ReadOnlyField(source='owner.username')
    
class UserSerializer(serializers.ModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(many=True, queryset=Post.objects.all())
    comments = serializers.PrimaryKeyRelatedField(many=True, queryset=Comment.objects.all())
    class Meta:
        model = User
        fields = ['id','username','posts', 'comments', 'avatar', 'created_at']