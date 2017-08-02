from django.conf.urls import url
from django.urls import reverse_lazy
from django.contrib import admin
from django.views.generic import RedirectView
from . import models, views

app_name = 'registry'
urlpatterns = [
    url(r'^$', views.object_list_view, {'model_name': 'project'}, name='front_page'),
    
    # List Views
    url(r'^projects/?$', views.object_list_view, {'model_name': 'project'}, name='project_list'),
    
    # Create Views
    url(r'^agent/new/?$', views.object_view, {'model_name': 'agent', 'pk': 'new'}, name='agent_create'),
    url(r'^project/new/?$', views.object_view, {'model_name': 'project', 'pk': 'new'}, name='project_create'),
    url(r'^seed/new/?$', views.object_view, {'model_name': 'seed', 'pk': 'new'}, name='seed_create'),
    
    # Update Views
    url(r'^agent/(?P<pk>\d+)/update/?$', views.object_view, {'model_name': 'agent'}, name='agent_update'),
    url(r'^project/(?P<pk>\d+)/update/?$', views.object_view, {'model_name': 'project'}, name='project_update'),
    url(r'^seed/(?P<pk>\d+)/update/?$', views.object_view, {'model_name': 'seed'}, name='seed_update'),
    
    # Detail Views
    url(r'^agent/(?P<pk>\d+)/?$', views.object_view, {'model_name': 'agent'}, name='agent_detail'),
    url(r'^project/(?P<pk>\d+)/?$', views.ProjectDetailView.as_view(), name='project_detail'),
    url(r'^seed/(?P<pk>\d+)/?$', views.object_view, {'model_name': 'seed'}, name='seed_detail'),
    
    # generic views using introspection -- replace these later
    url(r'^(?P<model_name>\w+)s/?$', views.object_list_view, name='object_list'),
    url(r'^(?P<model_name>\w+)/(?P<pk>\d+)$/?$', views.object_view, name='object_view'),
]