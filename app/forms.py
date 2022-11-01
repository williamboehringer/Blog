from django import forms
from app.models import Comments, Subscribe
from django.utils.translation import gettext_lazy as _

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['content', 'email', 'name', 'website']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs['placeholder'] = 'Type your comment'
        self.fields['email'].widget.attrs['placeholder'] = 'Type your Email'
        self.fields['name'].widget.attrs['placeholder'] = 'Type your Name'
        self.fields['website'].widget.attrs['placeholder'] = 'Type your Website'

class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscribe
        fields = '__all__'
        labels = {'email': _('')}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'Enter your Email'
       