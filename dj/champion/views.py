from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView
from django.shortcuts import render
from django.urls import reverse_lazy

from .forms import LinkForm
from .models import Link


class LinkListView(ListView):
    model = Link


class LinkCreateView(CreateView):
    model = Link
    form_class = LinkForm
    success_url = reverse_lazy('champion:index')

    def form_valid(self, form):
        link = form.save(commit=False)
        link.user = self.request.user
        return super().form_valid(form)
