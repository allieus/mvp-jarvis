from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy

from .forms import LinkForm
from .mixins import DocsTagRequiredMixin
from .models import Link


class LinkListView(ListView):
    model = Link


class LinkCreateView(DocsTagRequiredMixin, CreateView):
    model = Link
    form_class = LinkForm
    template_name = 'form.html'
    success_url = reverse_lazy('champion:index')

    def form_valid(self, form):
        link = form.save(commit=False)
        link.author = self.request.user
        if not link.label:
            link.update_label()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['author'] = self.request.user
        return kwargs
