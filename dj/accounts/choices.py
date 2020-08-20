from django.db.models import TextChoices


class LocaleChoices(TextChoices):
    AMERICAN = 'en-us', 'American (en-us)'
    KOREA = 'ko-kr', 'Korea, Republic Of (ko-kr)'
