from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.views.generic import CreateView

from accounts.forms import SignupForm


signup = CreateView.as_view(
    form_class=SignupForm,
    extra_context={'form_title': 'Signup'},
    template_name='form.html',
    success_url=settings.LOGIN_URL,
)


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
