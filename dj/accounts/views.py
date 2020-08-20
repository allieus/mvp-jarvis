from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from accounts.forms import ProfileForm
from accounts.models import Profile


login = LoginView.as_view(
    extra_context={'form_title': 'Login'},
    template_name='form.html',
)


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
