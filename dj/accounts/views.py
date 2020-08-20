from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from accounts.forms import SignupForm, ProfileForm
from accounts.models import Profile


class SignupView(CreateView):
    form_class = SignupForm
    extra_context = {'form_title': 'Signup'}
    template_name = 'form.html'
    success_url = reverse_lazy('profile_edit')

    def form_valid(self, form):
        response = super().form_valid(form)
        auth_login(self.request, self.object)
        messages.info(self.request, 'You are automatically logged in. Please enter your mvp id and docs tag.')
        return response


login = LoginView.as_view(
    extra_context={'form_title': 'Login'},
    template_name='form.html',
)


logout = LogoutView.as_view(
    next_page=settings.LOGIN_URL,
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
