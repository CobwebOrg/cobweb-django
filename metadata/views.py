from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from metadata import models, forms



class MDIndexView(ListView):
    model = models.Metadatum
    template_name = "project_list.html"

class MDDetailView(DetailView):
    model = models.Metadatum
    template_name = "project_detail.html"

class MDCreateView(LoginRequiredMixin, CreateView):
    model = models.Metadatum
    template_name = 'md_test.html'
    form_class = forms.MetadatumForm

    # def form_valid(self, form):
    #     candidate = form.save(commit=False)
    #     candidate.administered_by.add(self.request.user)

    #     candidate.save()
    #     return super().form_valid(form)

class MDUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Metadatum
    template_name = 'md_test.html'
    form_class = forms.MetadatumForm