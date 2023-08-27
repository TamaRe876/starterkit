from django.contrib import admin
from .models import NFT, Artist, Playlist, Charts, Genre, Tag

# Register your models here.
admin.site.register(NFT)
admin.site.register(Artist)
admin.site.register(Playlist)
admin.site.register(Charts)
admin.site.register(Genre)
admin.site.register(Tag)