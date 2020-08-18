import re
from django import forms
from .models import Link


class LinkForm(forms.ModelForm):
    valid_url_patterns = [
        r'^https?://docs.microsoft.com/.*',
    ]

    class Meta:
        model = Link
        fields = ['mvp_tag', 'url', 'label']

    def clean_mvp_tag(self):
        mvp_tag = self.cleaned_data.get('mvp_tag')
        if mvp_tag:
            if not re.match(r'[a-zA-Z]{2}-MVP-\d{7}', mvp_tag):
                raise forms.ValidationError('Invalid Identification tag.')
        return mvp_tag

    def clean_url(self):
        url = self.cleaned_data.get('url')
        if url:
            is_valid = any(
                re.match(url_pattern, url)
                for url_pattern in self.valid_url_patterns
            )
            if not is_valid:
                raise forms.ValidationError('Invalid host.')

        return url

    def clean(self):
        mvp_tag = self.cleaned_data.get('mvp_tag')
        url = self.cleaned_data.get('url')

        if mvp_tag and url:
            if Link.objects.filter(mvp_tag=mvp_tag, url=url).exists():
                raise forms.ValidationError("Already exists Link.")

        return self.cleaned_data
