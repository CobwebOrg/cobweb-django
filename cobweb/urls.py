from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, RedirectView

from . import models, views


urlpatterns = [
    url(r'^admin/?', admin.site.urls),
    
    url(r'^$', views.ProjectIndexView.as_view(), name='front_page'),
    
    # List Views
    url(r'^projects/?$', views.ProjectIndexView.as_view(), name='project_list'),
    
    # Create Views
    url('^register/', CreateView.as_view(
            template_name='generic_form.html',
            form_class=UserCreationForm,
            success_url='/',
    ), name='register'),
    url(r'^project/new/?$', views.ProjectCreateView.as_view(), name='project_create'),
    
    # Update Views
    url(r'^agent/(?P<pk>\d+)/update/?$', views.object_view, {'model_name': 'agent'}, name='agent_update'),
    url(r'^project/(?P<pk>\d+)/update/?$', views.object_view, {'model_name': 'project'}, name='project_update'),
    
    # Detail Views
    url(r'^agent/(?P<pk>\d+)/?$', views.object_view, {'model_name': 'agent'}, name='agent_detail'),
    url(r'^project/(?P<pk>\d+)/?$', views.ProjectDetailView.as_view(), name='project_detail'),
    url(r'^resource/(?P<pk>\d+)/?$', views.object_view, {'model_name': 'resource'}, name='resource_detail'),

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