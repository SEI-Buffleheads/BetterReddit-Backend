from django.contrib import admin
from .models import Post, Comment, User

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(User)
