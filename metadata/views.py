from dal import autocomplete
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView

from metadata import models  # , forms


class KeywordIndexView(ListView):
    model = models.Keyword
    template_name = "keyword_list.html"
    section = 'metadata'


class KeywordDetailView(DetailView):
    model = models.Keyword
    template_name = "keyword_detail.html"
    section = 'metadata'


class KeywordCreateView(LoginRequiredMixin, CreateView):
    model = models.Keyword
    template_name = 'md_test.html'
    # form_class = forms.KeywordForm
    section = 'metadata'


class KeywordAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return models.Keyword.objects.none()

        qs = models.Keyword.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs
