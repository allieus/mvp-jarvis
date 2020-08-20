from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy

from .forms import LinkForm
from .mixins import DocsTagRequiredMixin
from .models import Link


User = get_user_model()


class PublicLinkListView(ListView):
    model = Link


class LinkListView(ListView):
    model = Link

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(author__profile__mvp_id=self.kwargs['mvp_id'])
        return qs

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['author'] = get_object_or_404(User, profile__mvp_id=self.kwargs['mvp_id'])
        return context_data


class LinkCreateView(DocsTagRequiredMixin, CreateView):
    model = Link
    form_class = LinkForm
    template_name = 'form.html'
    success_url = reverse_lazy('champion:index')

    def form_valid(self, form):
        link = form.save(commit=False)
        link.author = self.request.user
        link.update_properties()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['author'] = self.request.user
        return kwargs
