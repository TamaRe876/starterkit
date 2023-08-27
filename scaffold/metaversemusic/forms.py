# forms.py

from django import forms
from .models import Playlist, Charts, NFT, Genre


class PlaylistForm(forms.ModelForm):
    tags = forms.CharField(max_length=100, required=False)  # Use CharField instead of MultipleChoiceField

    class Meta:
        model = Playlist
        fields = ['name', 'songs', 'tags']


class ChartsForm(forms.ModelForm):
    class Meta:
        model = Charts
        fields = '__all__'


class NFTForm(forms.ModelForm):
    class Meta:
        template = 'metaversemusic/create_nfts.html'
        model = NFT
        fields = [
            'title', 'description', 'image', 'music',
            'album', 'release_date', 'artist_name', 'minting_cost',
            'royalty_share', 'composer', 'duration'
        ]
        widgets = {
            'release_date': forms.DateInput(
                attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)', 'class': 'form-control'}
            )
        }


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['genre_choice']


class CombinedForm(forms.Form):
    nftform = NFTForm(prefix='nft')
    genreform = GenreForm(prefix='genre')
