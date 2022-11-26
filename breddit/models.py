from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.conf import settings

class Post(models.Model):
  owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts_by', on_delete=models.CASCADE, null=True)
  title = models.CharField(max_length=256)
  body = models.CharField(max_length=256)
  created_at = models.DateTimeField(default=datetime.now)
  link = models.URLField(default='', blank=True)
  votes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_posts', blank=True)
  
  def __str__(self):
    return self.title
  
class Comment(models.Model):
  owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments_by', on_delete=models.CASCADE, null=True)
  body = models.CharField(max_length=256)
  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='op')
  created_at = models.DateTimeField(default=datetime.now)
  votes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_comments', blank=True)
  
  def __str__(self):
    return self.owner

class UserManager(BaseUserManager):
  def create_user(self, username, password=None, **kwargs):
    if username is None:
      raise TypeError('Need a Username')
    user = self.model(username=username)
    user.set_password(password)
    user.save(using=self._db)
    return user
  
  def create_superuser(self, username, password, email=None):
    if password is None:
      raise TypeError("Need Password")
    if username is None:
      raise TypeError("Need Username")
    user = self.create_user(username, password)
    user.is_superuser = True
    user.is_staff = True
    user.save(using=self._db)
    return user
    
class User(AbstractUser, PermissionsMixin):
  created_at = models.DateTimeField(default=datetime.now)
  avatar = models.ImageField(upload_to='avatars', default='default-avatar.png')
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)
  favorites = models.ManyToManyField(Post, related_name='favorited', blank=True)
  
  objects = UserManager()
  
  def __str__(self):
    return self.username


