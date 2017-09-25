from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.forms import ModelForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, RedirectView

from core.views import UserIndexView, UserDetailView, UserCreateView, UserUpdateView, AgentDetailView
from projects.views import ProjectIndexView, ProjectDetailView, ProjectCreateView
from projects.views import NominationDetailView, NominationCreateView

urlpatterns = [
    url(r'^admin/?', admin.site.urls),
    
    url(r'^$', ProjectIndexView.as_view(), name='front_page'),
    
    # User
    url(r'^users/', UserIndexView.as_view(), name='user_list'),
    url(r'^user/(?P<pk>\d+)/?$', UserDetailView.as_view(), name='user_detail'),
    url(r'^user/new/?$', UserCreateView.as_view(), name='user_create'),
    # url(r'^users/(?P<pk>\d+)/update/?$', UserUpdateView.as_view(), name='user_update'),

    # Agent
    url(r'^agent/(?P<pk>\d+)/?$', AgentDetailView.as_view(), name='agent_detail'),

    # Project
    url(r'^projects/?$', ProjectIndexView.as_view(), name='project_list'),
    url(r'^project/(?P<pk>\d+)/?$', ProjectDetailView.as_view(), name='project_detail'),
    url(r'^project/new/?$', ProjectCreateView.as_view(), name='project_create'),
    # url(r'^project/(?P<pk>\d+)/update/?$', ProjectUpdateView.as_view(), name='project_update'),
    
    # Nomination
    url(r'^nomination/(?P<pk>\d+)/', NominationDetailView.as_view(), name='nomination_detail'),
    url(r'^project/(?P<project_id>\d+)/nominate/', NominationCreateView.as_view(), name='nominate'),

    # Resource

    # Auth
    url(r'^', include('django.contrib.auth.urls')),
]


# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns = [
#         url(r'^__debug__/', include(debug_toolbar.urls)),
#     ] + urlpatterns