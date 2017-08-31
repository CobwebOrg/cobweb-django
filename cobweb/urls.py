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
    url(r'^users/', views.UserIndexView.as_view(), name='user_list'),
    url(r'^user/(?P<pk>\d+)/?$', views.UserDetailView.as_view(), name='user_detail'),
    url(r'^user/new/?$', views.UserCreateView.as_view(), name='user_create'),
    # url(r'^users/(?P<pk>\d+)/update/?$', views.UserUpdateView.as_view(), name='user_update'),

    # Agent
    url(r'^agent/(?P<pk>\d+)/?$', views.AgentDetailView.as_view(), name='agent_detail'),

    # Project
    url(r'^projects/?$', views.ProjectIndexView.as_view(), name='project_list'),
    url(r'^project/(?P<pk>\d+)/?$', views.ProjectDetailView.as_view(), name='project_detail'),
    url(r'^project/new/?$', views.ProjectCreateView.as_view(), name='project_create'),
    # url(r'^project/(?P<pk>\d+)/update/?$', views.ProjectUpdateView.as_view(), name='project_update'),
    
    # Nomination
    url(r'^nomination/(?P<pk>\d+)/', views.NominationDetailView.as_view(), name='nomination_detail'),
    url(r'^nominate/', views.NominationCreateView.as_view(), name='nominate'),

    # Resource

    # Auth
    url(r'^', include('django.contrib.auth.urls')),
]


# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns = [
#         url(r'^__debug__/', include(debug_toolbar.urls)),
#     ] + urlpatterns