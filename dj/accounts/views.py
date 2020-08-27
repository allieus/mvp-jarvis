from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from accounts.forms import ProfileForm
from accounts.models import Profile


def login(request):
    if 'allauth.socialaccount.providers.github' in settings.INSTALLED_APPS:
        return redirect('/accounts/github/login/')
    raise Http404


logout = LogoutView.as_view(
    next_page=reverse_lazy('root'),
)


@login_required
def profile(request):
    return render(request, 'accounts/profile.html')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'form.html'
    extra_context = {'form_title': 'Edit Profile'}
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        try:
            return self.request.user.profile
        except Profile.DoesNotExist:
            return Profile.objects.create(user=self.request.user)
