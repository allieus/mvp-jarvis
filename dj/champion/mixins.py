from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect

from accounts.models import Profile


class DocsTagRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        try:
            docs_tag = request.user.profile.docs_tag
        except Profile.DoesNotExist:
            docs_tag = None

        if not docs_tag:
            messages.error(request, f'Please enter Docs Champion identification tag.')
            return redirect('profile')

        return super().dispatch(request, *args, **kwargs)
