from django.db import models
from django.contrib.auth.models import User


class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    song_ids = models.ManyToManyField('blog.Post', related_name='playlists')
    tags = models.ManyToManyField('Tag', related_name='playlists')
    saved_by = models.ManyToManyField(User, related_name='saved_playlists')

    def __str__(self):
        return self.name


class Charts(models.Model):
    post = models.OneToOneField('blog.Post', on_delete=models.CASCADE, primary_key=True)
    likes_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    saves_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.post)


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
