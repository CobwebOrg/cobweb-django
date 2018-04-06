from dal import autocomplete
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView

from metadata import models  # , forms


class TagIndexView(ListView):
    model = models.Tag
    template_name = "tag_list.html"
    section = 'metadata'


class TagDetailView(DetailView):
    model = models.Tag
    template_name = "tag_detail.html"
    section = 'metadata'


class TagCreateView(LoginRequiredMixin, CreateView):
    model = models.Tag
    template_name = 'md_test.html'
    # form_class = forms.TagForm
    section = 'metadata'


class TagAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return models.Tag.objects.none()

        qs = models.Tag.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs
