from django.conf.urls import url
from django.contrib import admin
from django.views import generic
from . import models, views

app_name = 'registry'
urlpatterns = [
    # url(r'^$', views.projectindexview, name='project_index'),
    url(r'^project/(?P<pk>.+)$/?', views.ProjectDetailView.as_view(), name='project_detail'),
    
    # generic views using introspection -- replace these later
    url(r'^(?P<model_name>\w+)/?', views.object_list_view, name='object_list'),
    url(r'^(?P<model_name>\w+)/(?P<pk>.+)$/?', views.object_view, name='object_view'),
]