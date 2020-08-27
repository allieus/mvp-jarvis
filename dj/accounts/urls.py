from django.conf import settings
from django.http import Http404
from django.shortcuts import redirect
from django.urls import path

from . import views


def login(request):
    if 'allauth.socialaccount.providers.github' in settings.INSTALLED_APPS:
        return redirect('/accounts/github/login/')
    raise Http404


urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='profile_edit'),
]
