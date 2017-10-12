from django.conf.urls import url

from webresources import views

app_name = 'webresources'
urlpatterns = [
    url(r'^$', views.ResourceListView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$', views.ResourceDetailView.as_view(), name='detail'),
]

