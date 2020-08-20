from django.contrib.auth.base_user import AbstractBaseUser
from django.core.mail import send_mail
from django.core.validators import RegexValidator, EmailValidator
from django.contrib.auth.models import (
    UserManager, PermissionsMixin
)
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[EmailValidator()],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    name = models.CharField(_('name'), max_length=50, db_index=True, blank=True)
    email = models.EmailField(_('email address'), blank=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.username = self.__class__.objects.normalize_email(self.username)

    def get_full_name(self):
        return self.name.strip()

    def get_short_name(self):
        return self.name.strip()

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mvp_id = models.CharField(max_length=7, validators=[RegexValidator(r'\d{7}')], blank=True,
                              help_text='Please enter 7 digits. ex) 1234567')
    docs_tag = models.CharField(max_length=14, validators=[RegexValidator(r'[a-zA-Z]{2}-[mM][vV][pP]-\d{7}')],
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
