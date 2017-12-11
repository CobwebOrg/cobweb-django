from django.views.generic import ListView, DetailView

from archives import models


class CollectionIndexView(ListView):
    model = models.Collection
    template_name = "archives/collection_list.html"


class CollectionDetailView(DetailView):
    model = models.Collection
    template_name = "archives/collection.html"