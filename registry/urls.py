from django.conf.urls import url
from django.views import generic
from . import models, views

app_name = 'registry'
urlpatterns = [
    url(r'^$', views.ProjectIndexView.as_view(), name='project_index'),
    # url(r'^project/(?P<pk>\d+)', views.ProjectDetailView.as_view(), name='project_detail'),
    url(r'^(?P<model_name>\w+)/?$', views.object_list, name='object_list'),
    url(r'^(?P<model_name>.+)/(?P<pk>.+)$', views.object_view, name='object_view'),
    # url(r'^(?P<model_name>.+)/(?P<pk>.+)/save$', views.save_object, name='save_object'),
    # url(r'^(?institution/P<id>[0-9]+)/$', , name='detail'),
]