from django.db import models
from datetime import date

class Post(models.Model):
  owner = models.ForeignKey('auth.User', related_name='posts', on_delete=models.CASCADE, null=True)
  title = models.CharField(max_length=256)
  body = models.CharField(max_length=256)
  datetime = models.DateTimeField(auto_now=True)
  up_votes = models.IntegerField(blank=True, null=True)
  
  def __str__(self):
    return self.title
  
class Comment(models.Model):
  owner = models.ForeignKey('auth.User', related_name='comments', on_delete=models.CASCADE, null=True)
  body = models.CharField(max_length=256)
  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='posts')
  datetime = models.DateTimeField(auto_now=True)
  all_votes = models.IntegerField(blank=True, null=True)
  
  def __str__(self):
    return self.owner

