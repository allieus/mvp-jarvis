from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

from django.db import models


class Link(models.Model):
    mvp_tag = models.CharField(max_length=20, db_index=True, help_text='ex) AI-MVP-1234567')
    url = models.URLField()
    label = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def tagged_url(self):
        parse_result = urlparse(self.url)
        params = dict(parse_qsl(parse_result.query))
        params['WT.mc_id'] = self.mvp_tag
        return urlunparse(parse_result._replace(query=urlencode(params)))

    class Meta:
        unique_together = [
            ('mvp_tag', 'url'),
        ]
        ordering = ['-id']
