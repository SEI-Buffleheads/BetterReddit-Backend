from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
  created_at = models.DateTimeField(default=datetime.now)
  avatar = models.ImageField(upload_to='avatars', default='default-avatar.png')
  
  def __str__(self):
    return self.username

class Post(models.Model):
  owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts', on_delete=models.CASCADE, null=True)
  title = models.CharField(max_length=256)
  body = models.CharField(max_length=256)
  created_at = models.DateTimeField(default=datetime.now)
  votes = models.IntegerField(blank=True, null=True)
  
  def __str__(self):
    return self.title
  
class Comment(models.Model):
  owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments', on_delete=models.CASCADE, null=True)
  body = models.CharField(max_length=256)
  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='posts')
  created_at = models.DateTimeField(default=datetime.now)
  votes = models.IntegerField(blank=True, null=True)
  
  def __str__(self):
    return self.owner

