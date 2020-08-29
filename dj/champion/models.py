from logging import getLogger
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

import requests
from bs4 import BeautifulSoup
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property
from jsonfield import JSONField as JSONTextField
from requests import Timeout

from accounts.choices import LocaleChoices
from accounts.models import Profile


logger = getLogger(__name__)


class Link(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    url = models.URLField('Share Docs URL')
    title = models.CharField(max_length=200, blank=True)
    properties = JSONTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('champion:link_detail', args=[self.pk])

    @cached_property
    def tagged_url(self):
        profile: Profile = self.author.profile

        parse_result = urlparse(self.url)
        params = dict(parse_qsl(parse_result.query))
        params['WT.mc_id'] = profile.docs_tag

        return urlunparse(parse_result._replace(query=urlencode(params)))

    def update_properties(self):
        try:
            res = requests.get(self.url, timeout=3)
        except Timeout as e:
            logger.error(e)
        else:
            if res.encoding == 'ISO-8859-1':
                res.encoding = 'utf8'
            soup = BeautifulSoup(res.text, 'html.parser')

            properties = {}
            for tag in soup.select('meta[property^=og]'):
                key = tag['property'].replace('og:', '')
                value = tag['content']
                properties[key] = value

            if 'title' not in properties:
                title_tag = soup.select_one('title')
                if title_tag:
                    properties['title'] = title_tag.text
                else:
                    properties['title'] = 'Not found title'

            self.title = properties.get('title', '')
            self.properties = properties

    class Meta:
        unique_together = [
            ('author', 'url'),
        ]
        ordering = ['-id']
