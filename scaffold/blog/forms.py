from django import forms
from .models import Comment, Post, SupportMessage


class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control custom-txt', 'cols': '40', 'rows': '3'}),
                           label='')

    class Meta:
        model = Comment
        fields = ['body']


class PostForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}), label='')
    caption = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Caption'}), label='')
    link = forms.FileField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter song URL'}
                                                  ))
    vibe = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
                                 label='Video')

    class Meta:
        model = Post
        fields = ['title', 'link', 'vibe', 'caption']



class SupportMessageForm(forms.ModelForm):
    class Meta:
        model = SupportMessage
        fields = ['message']