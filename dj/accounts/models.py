from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.validators import RegexValidator
from django.db import models

from accounts.choices import LocaleChoices


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mvp_id = models.CharField(max_length=7, validators=[RegexValidator(r'\d{4,7}')], blank=True,
                              help_text='Please enter digits. ex) 1234567')
    docs_tag = models.CharField(max_length=20, validators=[RegexValidator(r'[a-zA-Z]{2,5}-[mM][vV][pP]-\d{4,7}')],
                                blank=True, help_text='Docs Champion Identification Tag. ex) AZ-MVP-1234567')
    bio = models.TextField(blank=True)

    @property
    def public_profile_url(self) -> str:
        if not self.mvp_id:
            return ""
        return f"https://mvp.microsoft.com/en-us/PublicProfile/{self.mvp_id}"

    @property
    def public_photo_url(self) -> str:
        if not self.mvp_id:
            return ""
        return f"https://mvp.microsoft.com/en-us/PublicProfile/Photo/{self.mvp_id}"
