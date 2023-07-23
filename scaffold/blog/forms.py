from django import forms
from .models import Comment, Post


class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control custom-txt', 'cols': '40', 'rows': '3'}),
                           label='')

    class Meta:
        model = Comment
        fields = ['body']


class PostForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}), label='')
    song = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}), label='Song')
    cover_art = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
                                 label='Cover Art')

    class Meta:
        model = Post
        fields = ['title', 'song', 'cover_art']
