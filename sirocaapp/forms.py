from django import forms
from django.core.exceptions import ValidationError

from .models import *


class IndexForm(forms.ModelForm):
    class Meta:
        model = UserRequest
        fields = ['url']

    def clean_url(self):
        new_url = self.cleaned_data['url']
        if new_url.startswith('https://github.com'):
            return new_url
        raise ValidationError('url must be start with "https://github.com/"')