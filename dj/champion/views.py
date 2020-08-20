from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .forms import LinkForm
from .mixins import DocsTagRequiredMixin
from .models import Link


User = get_user_model()


class PublicLinkListView(ListView):
    model = Link
    paginate_by = 100

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(title__icontains=q)
        return qs


class LinkListView(ListView):
    model = Link
    paginate_by = 100

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(author__profile__mvp_id=self.kwargs['mvp_id'])
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(title__icontains=q)
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

    def get_initial(self):
        initial = super().get_initial()
        if self.request.user.profile.prefer_locale:
            initial['locale'] = self.request.user.profile.prefer_locale
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['author'] = self.request.user
        return kwargs

    def get_success_url(self):
        messages.success(self.request, f'Link was created successfully.')
        return super().get_success_url()


class LinkUpdateView(DocsTagRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Link
    form_class = LinkForm
    template_name = 'form.html'
    success_url = reverse_lazy('champion:index')

    def test_func(self):
        return self.request.user == self.get_object().author

    def form_valid(self, form):
        link = form.save(commit=False)
        link.update_properties()
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, f'Link was updated successfully.')
        return super().get_success_url()


class LinkDeleteView(DocsTagRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Link
    success_url = reverse_lazy('champion:index')

    def test_func(self):
        return self.request.user == self.get_object().author

    def get_success_url(self):
        messages.success(self.request, f'Link was deleted successfully.')
        return super().get_success_url()
