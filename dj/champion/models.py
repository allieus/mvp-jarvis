from logging import getLogger
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

import requests
from bs4 import BeautifulSoup
from django.conf import settings
from django.db import models
from django.utils.functional import cached_property
from requests import Timeout

from accounts.models import Profile


logger = getLogger(__name__)


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

        return urlunparse(parse_result._replace(query=urlencode(params)))

    def update_label(self):
        try:
            res = requests.get(self.url, timeout=3)
        except Timeout as e:
            logger.error(e)
        else:
            if res.encoding == 'ISO-8859-1':
                res.encoding = 'utf8'
            soup = BeautifulSoup(res.text, 'html.parser')
            og_tag = soup.select_one('meta[property="og:title"]')
            title_tag = soup.select_one('title')
            if og_tag:
                label = og_tag['content']
            elif title_tag:
                label = title_tag.text
            else:
                label = 'Not found title'

            self.label = label

    class Meta:
        unique_together = [
            ('author', 'url'),
        ]
        ordering = ['-id']
