from django.conf.urls import url
from django.urls import path

from archives import views


app_name = 'archives'
urlpatterns = [
    url(r'^$', views.CollectionIndexView.as_view(),
        name='collection_list'),
    url(r'^(?P<pk>\d+)/$',
        views.CollectionDetailView.as_view(),
        name='collection_detail'),
    path('<pk>/edit',
         views.CollectionUpdateView.as_view(),
         name='collection_update'),

    # Claim
    path('autocomplete',
         views.CollectionAutocomplete.as_view(),
         name='collection_autocomplete'),
]
