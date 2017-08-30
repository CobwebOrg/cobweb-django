from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.forms import ModelForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, RedirectView

from . import models, views


urlpatterns = [
    url(r'^admin/?', admin.site.urls),
    
    url(r'^$', views.ProjectIndexView.as_view(), name='front_page'),
    
    # User
    url('^users/', views.UserIndexView.as_view(), name='user_list'),
    url('^users/(?P<pk>\d+)/?$', views.UserDetailView.as_view(), name='user_detail'),
    url('^users/new/?$', views.UserCreateView.as_view(), name='user_create'),
    # url('^users/(?P<pk>\d+)/update/?$', views.UserUpdateView.as_view(), name='user_update'),

    url(r'^agent/(?P<pk>\d+)/update/?$', views.object_view, {'model_name': 'agent'}, name='agent_update'),
    url(r'^agent/(?P<pk>\d+)/?$', views.object_view, {'model_name': 'agent'}, name='agent_detail'),

    # Project
    url(r'^projects/?$', views.ProjectIndexView.as_view(), name='project_list'),
    url(r'^project/(?P<pk>\d+)/?$', views.ProjectDetailView.as_view(), name='project_detail'),
    url(r'^project/new/?$', views.ProjectCreateView.as_view(), name='project_create'),
    url(r'^project/(?P<pk>\d+)/update/?$', views.object_view, {'model_name': 'project'}, name='project_update'),
    
    # Resource
    url(r'^resource/(?P<pk>\d+)/?$', views.object_view, {'model_name': 'resource'}, name='resource_detail'),

    # Auth
    url('^', include('django.contrib.auth.urls')),
    
    # generic views using introspection -- replace these later
    # url(r'^(?P<model_name>\w+)s/?$', views.object_list_view, name='object_list'),
    # url(r'^(?P<model_name>\w+)/(?P<pk>\d+)$/?$', views.object_view, name='object_view'),
]


# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns = [
#         url(r'^__debug__/', include(debug_toolbar.urls)),
#     ] + urlpatterns