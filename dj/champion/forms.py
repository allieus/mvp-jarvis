import re
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

from django import forms
from .models import Link


class LinkForm(forms.ModelForm):
    valid_url_patterns = [
        r'^https?://docs.microsoft.com/.*',
    ]

    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author')
        super().__init__(*args, **kwargs)

    def clean_url(self):
        url = self.cleaned_data.get('url')
        if url:
            is_valid = any(
                re.match(url_pattern, url)
                for url_pattern in self.valid_url_patterns
            )
            if not is_valid:
                raise forms.ValidationError('Invalid host.')

            parse_result = urlparse(url)
            params = dict(parse_qsl(parse_result.query))
            if 'fbclid' in params:
                del params['fbclid']

            url = urlunparse(parse_result._replace(query=urlencode(params)))

        return re.sub(r'#/$', '', url)

    def clean(self):
        url = self.cleaned_data.get('url')

        if self.author and url:
            if Link.objects.filter(author=self.author, url=url).exists():
                raise forms.ValidationError("You have already registered URL.")

        return self.cleaned_data

    class Meta:
        model = Link
        fields = ['url']
