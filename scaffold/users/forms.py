from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from PIL import Image
from django_countries.widgets import CountrySelectWidget
from django_countries.fields import CountryField



class UserRegisterForm(UserCreationForm):
    USER_TYPE_CHOICES = (
        ('artist', 'Artist'),
        ('fan', 'Fan'),
    )

    email = forms.EmailField()
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, initial='fan', widget=forms.RadioSelect)
    country = CountryField()

    class Meta:
        model = User
        widgets = {"country": CountrySelectWidget()}
        date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']



    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

        user_profile = Profile.objects.create(user=user, country=self.cleaned_data['country'], user_type=self.cleaned_data['user_type'], date_of_birth=self.cleaned_data['date_of_birth'])
        return user, user_profile



class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name','last_name','username','email']


class ProfileUpdateForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput(), required=False)
    y = forms.FloatField(widget=forms.HiddenInput(), required=False)
    width = forms.FloatField(widget=forms.HiddenInput(), required=False)
    height = forms.FloatField(widget=forms.HiddenInput(), required=False)

    image = forms.ImageField(label=('Image'), error_messages = {'invalid':("Image files only")}, widget=forms.FileInput, required=False)
    class Meta:
        model = Profile
        fields = ['bio','date_of_birth','image',]


    """Saving Cropped Image"""
    def save(self,*args,**kwargs):
        img = super(ProfileUpdateForm, self).save(*args, **kwargs)

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        if x and y and w and h:
            image = Image.open(img.image)
            cropped_image = image.crop((x, y, w+x, h+y))
            resized_image = cropped_image.resize((300, 300), Image.ANTIALIAS)
            resized_image.save(img.image.path)

        return img