from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField

""" Model for User Profile """


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_online = models.BooleanField(default=False)
    is_artist = models.BooleanField(default=False)
    following = models.ManyToManyField(User, related_name="following", blank=True)
    friends = models.ManyToManyField(User, related_name='my_friends', blank=True)
    country = CountryField(blank_label="(select country)", default='JM')
    bio = models.CharField(default="", blank=True, null=True, max_length=350)
    bnb_wallet_address = models.CharField(max_length=42, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics', blank=True, null=True)

    def profile_posts(self):
        return self.user.post_set.all()

    def get_friends(self):
        return self.friends.all()

    def get_friends_no(self):
        return self.friends.all().count()

    def __str__(self):
        return f'{self.user.username} Profile'


STATUS_CHOICES = (
    ('send', 'send'),
    ('accepted', 'accepted')
)


class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='friend_sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='friend_receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"


class UserType(models.Model):
    USER_TYPE_CHOICES = (
        ('artist', 'Artist'),
        ('fan', 'Fan'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='fan')

    def __str__(self):
        return self.user_type
