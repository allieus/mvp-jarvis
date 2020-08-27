import re
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

from django import forms
from .models import Link


class LinkForm(forms.ModelForm):
    allowed_host_list = list(map(
        lambda host: host.replace('.', r'\.'), [
            'docs.microsoft.com',
            'social.technet.microsoft.com',
            'azure.microsoft.com',
            'techcommunity.microsoft.com',
            'social.msdn.microsoft.com',
            'devblogs.microsoft.com',
            'developer.microsoft.com',
            'channel9.msdn.com',
            'gallery.technet.microsoft.com',
            'cloudblogs.microsoft.com',
            'technet.microsoft.com',
            'msdn.microsoft.com',
            'blogs.msdn.microsoft.com',
            'blogs.technet.microsoft.com',
        ]))

    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author', None)
        super().__init__(*args, **kwargs)

    def clean_url(self):
        url = self.cleaned_data.get('url')
        if url:
            # Ensure https:// scheme.
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            url = re.sub(r'^http://', 'https://', url)

            is_valid = any(
                re.match(r'https?://' + url_pattern + '/.*', url)
                for url_pattern in self.allowed_host_list
            )
            if not is_valid:
                raise forms.ValidationError('Invalid host in url.')

            parse_result = urlparse(url)
            params = dict(parse_qsl(parse_result.query))

            params = {
                key: value
                for key, value in params.items()
                if key.lower() not in (
                    'fbclid'.lower(),
                    'WT.mc_id'.lower(),
                )
            }

            url = urlunparse(parse_result._replace(query=urlencode(params)))

            # remove locale
            for host in self.allowed_host_list:
                pattern = '(' + host + ')' + r'/([a-z]{2}-[a-z]{2})/'
                if re.search(pattern, url):
                    url = re.sub(pattern, r'\1/', url)
                    break

        return re.sub(r'#/$', '', url)

    def clean(self):
        url = self.cleaned_data.get('url')

        if self.author and url:
            if Link.objects.filter(author=self.author, url=url).exists():
                raise forms.ValidationError('You have already registered URL.')
        elif self.instance and url:
            qs = Link.objects \
                .filter(author=self.instance.author, url=url) \
                .exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError('You have already registered URL.')

        self.cleaned_data['url'] = url

        return self.cleaned_data

    class Meta:
        model = Link
        fields = ['url']
