from .models import Post, Comment, User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import update_last_login
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.password_validation import validate_password

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
    favorites = serializers.StringRelatedField(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ['id','username','posts', 'comments', 'avatar', 'date_joined', 'is_active', 'favorites', 'last_login', 'updated_at']
        read_only_field = ['date_joined', 'is_active', 'last_login']

class LoginSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['user'] = UserSerializer(self.user).data
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data

class RegisterSerializer(UserSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True, required=True)
    username = serializers.CharField(max_length=128, required=True)

    class Meta:
        model = User
        fields = ['id','username','password', 'avatar', 'date_joined', 'is_active']

    def create(self, validated_data):
        try:
            user = User.objects.get(username=validated_data['username'])
            user = None
        except ObjectDoesNotExist:
            user = User.objects.create_user(**validated_data)
        return user

class ChangePasswordSerializer(serializers.Serializer):
    model = User
    new_password = serializers.CharField(max_length=128, min_length=8, required=True)
    old_password = serializers.CharField(required=True)
    

class UpdateAvatarSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('avatar',)

    def update(self, instance, validated_data):
        user = self.context['request'].user

        if user.pk != instance.pk:
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})

        instance.avatar = validated_data['avatar']

        instance.save()

        return instance