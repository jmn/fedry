from django import forms
from fd.models import FeedSource, Feed

class SourceCreateForm(forms.ModelForm):
    url = forms.URLField()
    class Meta:
        model = FeedSource
        fields = ['title', 'tags']
        
