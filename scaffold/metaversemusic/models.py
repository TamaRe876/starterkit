import os

from django.db import models
from django.contrib.auth.models import User
from mutagen.mp3 import MP3  # For MP3 files
from mutagen.oggvorbis import OggVorbis  # For OGG files
from mutagen.flac import FLAC  # For FLAC files
from web3 import Web3, HTTPProvider


class Genre(models.Model):
    DANCEHALL = 'Dancehall'
    HIPHOP = 'Hip Hop'
    REGGAE = 'Reggae'
    TRINIDANCEHALL = 'Trini Dancehall'
    TRAP = 'Trap'
    SOCA = 'Soca'
    CALYPSO = 'Calypso'
    SAMBA = 'Samba'
    AFROBEAT = 'Afro Beat'
    RNB = 'RnB'
    HOUSE = 'House'
    ELECTRONIC = 'Electronic'
    ROCK = 'Rock'
    COUNTRY = 'Country'

    GENRE_CHOICES = [
        (DANCEHALL, 'Dancehall'),
        (HIPHOP, 'Hip Hop'),
        (REGGAE, 'Reggae'),
        (TRINIDANCEHALL, 'Trini Dancehall'),
        (TRAP, 'Trap'),
        (SOCA, 'Soca'),
        (CALYPSO, 'Calypso'),
        (SAMBA, 'Samba'),
        (AFROBEAT, 'Afro Beat'),
        (RNB, 'RnB'),
        (HOUSE, 'House'),
        (ELECTRONIC, 'Electronic'),
        (ROCK, 'Rock'),
        (COUNTRY, 'Country'),
    ]

    genre_choice = models.CharField(max_length=20, choices=GENRE_CHOICES, default=DANCEHALL)

    def __str__(self):
        return self.genre_choice


# Create a Web3 instance for the Binance Smart Chain
web3 = Web3(Web3.HTTPProvider("https://bsc-dataseed.binance.org"))


# Create a model for the NFTs
class NFT(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='nfts')
    music = models.FileField(upload_to='nfts')
    album = models.CharField(max_length=200, blank=True, null=True)
    release_date = models.DateTimeField(auto_now=False)
    artist_name = models.CharField(max_length=100, blank=True, null=True)
    genre = models.ManyToManyField(Genre, blank=True, related_name="genre")
    duration = models.CharField(max_length=20, blank=True, null=True)
    composer = models.CharField(max_length=100, blank=True, null=True)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    token_id = models.BigIntegerField()
    # New fields for minting details
    minting_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    royalty_share = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    def get_media_type(self):
        if self.music:
            _, ext = os.path.splitext(self.music.name)
            if ext.lower() in ['.mp3', '.wav', '.ogg']:
                return 'song'
            elif ext.lower() in ['.jpg', '.jpeg', '.png', '.gif']:
                return 'picture'
            elif ext.lower() in ['.mp4', '.avi', '.mov']:
                return 'video'
        return ''

    def get_duration_as_string(self):
        if self.duration:
            duration_in_seconds = int(self.duration)
            minutes, seconds = divmod(duration_in_seconds, 60)
            return f"{minutes:02d}:{seconds:02d}"
        return "00:00"

    def save(self, *args, **kwargs):
        if self.music:
            audio = None

            try:
                if self.music.name.endswith('.mp3'):
                    audio = MP3(self.music.path)
                elif self.music.name.endswith('.ogg'):
                    audio = OggVorbis(self.music.path)
                elif self.music.name.endswith('.flac'):
                    audio = FLAC(self.music.path)

                if audio:
                    self.duration = audio.info.length
            except Exception as e:
                # Handle any potential errors when reading the audio file
                pass

        super(NFT, self).save(*args, **kwargs)


class Artist(models.Model):
    artist_name = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    nfts = models.ManyToManyField(NFT, related_name='artists')

    def __str__(self):
        return self.artist_name


class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    songs = models.ManyToManyField(NFT, related_name='playlists')

    def __str__(self):
        return self.name


class Charts(models.Model):
    post = models.OneToOneField(NFT, on_delete=models.CASCADE, primary_key=True)
    likes_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    saves_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.post)


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
