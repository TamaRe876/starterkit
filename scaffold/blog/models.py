from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
import os


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=150)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    vibe = models.FileField(upload_to='vibes/', blank=True, null=True)
    caption = models.TextField(max_length=500, blank=True, null=True)
    link = models.URLField(default='https://www.vibstream.com')
    tags = models.ManyToManyField(Tag, blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name="blogpost", blank=True)
    saves = models.ManyToManyField(User, related_name="blogsave", blank=True)

    def get_media_type(self):
        if self.vibe:
            _, ext = os.path.splitext(self.vibe.name)
            if ext.lower() in ['.mp3', '.wav', '.ogg']:
                return 'song'
            elif ext.lower() in ['.jpg', '.jpeg', '.png', '.gif']:
                return 'picture'
            elif ext.lower() in ['.mp4', '.avi', '.mov']:
                return 'video'
        return ''

    def total_likes(self):
        return self.likes.count()

    def total_saves(self):
        return self.saves.count()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={"pk": self.pk})


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="blogcomment", blank=True)
    reply = models.ForeignKey('self', null=True, related_name="replies", on_delete=models.CASCADE)

    def total_clikes(self):
        return self.likes.count()

    def __str__(self):
        return '%s - %s - %s' % (self.post.title, self.name, self.id)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={"pk": self.pk})


class SupportMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    responded = models.BooleanField(default=False)
    admin_response = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.timestamp}"