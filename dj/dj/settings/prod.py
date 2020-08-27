from .common import *

INSTALLED_APPS += [
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1

SOCIALACCOUNT_PROVIDERS = {
    'github': {
        'SCOPE': [
            'read:user',
        ],
        'APP': {
            'client_id': env.str('GITHUB_CLIENT_ID'),
            'secret': env.str('GITHUB_CLIENT_SECRET'),
            'key': ''
        }
    },
}
