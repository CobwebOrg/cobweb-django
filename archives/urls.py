from django.conf.urls import url

from archives import views


app_name = 'archives'
urlpatterns = [
    url(r'^$', views.CollectionIndexView.as_view(),
        name='collection_list'),
    url(r'^(?P<pk>\d+)/$',
        views.CollectionDetailView.as_view(),
        name='collection_detail'),
    url(r'^(?P<pk>\d+)/edit/$',
        views.CollectionUpdateView.as_view(),
        name='collection_update'),
]
