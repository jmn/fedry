from django import forms
from fd.models import FeedSource, Feed
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SourceCreateForm(forms.ModelForm):
    url = forms.URLField()
    class Meta:
        model = FeedSource
        fields = ['title', 'tags']
        
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
