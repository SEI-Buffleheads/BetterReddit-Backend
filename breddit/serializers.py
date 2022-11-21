from .models import Post, Comment
from django.contrib.auth.models import User
from rest_framework import serializers

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
        fields = ['id','username','posts', 'comments']