from django.contrib import admin
from .models import Comment, Post, SupportMessage

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(SupportMessage)
