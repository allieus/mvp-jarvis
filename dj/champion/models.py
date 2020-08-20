from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

from django.conf import settings
from django.db import models
from django.utils.functional import cached_property

from accounts.models import Profile


class Link(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    url = models.URLField('Share Docs URL')
    label = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @cached_property
    def tagged_url(self):
        profile: Profile = self.author.profile

        parse_result = urlparse(self.url)
        params = dict(parse_qsl(parse_result.query))
        params['WT.mc_id'] = profile.docs_tag

        if 'fbclid' in params:
            del params['fbclid']

        return urlunparse(parse_result._replace(query=urlencode(params)))

    class Meta:
        unique_together = [
            ('author', 'url'),
        ]
        ordering = ['-id']
