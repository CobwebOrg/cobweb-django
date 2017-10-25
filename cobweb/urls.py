from ajax_select import urls as ajax_select_urls
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.forms import ModelForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, RedirectView

from core.views import UserIndexView, UserDetailView, UserCreateView, UserUpdateView
import projects.views, metadata.views


urlpatterns = [
    url(r'^search/', include('haystack.urls')),
    
    url(r'^$', projects.views.ProjectIndexView.as_view(), name='front_page'),
    
    # User
    url(r'^users/(?P<pk>\d+)/edit/$', UserUpdateView.as_view(), name='user_update'),
    url(r'^users/(?P<pk>\d+)/$', UserDetailView.as_view(), name='user_detail'),
    url(r'^users/new$', UserCreateView.as_view(), name='user_create'),
    url(r'^users/$', UserIndexView.as_view(), name='user_list'),

    # Project
    url(r'^projects/$', 
        projects.views.ProjectIndexView.as_view(),
        name='project_list'),
    url(r'^projects/(?P<pk>\d+)/$', 
        projects.views.ProjectDetailView.as_view(),
        name='project_detail'),
    url(r'^projects/new$', 
        projects.views.ProjectCreateView.as_view(),
        name='project_create'),
    url(r'^projects/(?P<pk>\d+)/edit/$', 
        projects.views.ProjectUpdateView.as_view(), 
        name='project_update'),
    
    # Nomination
    url(r'^nomination/(?P<pk>\d+)/$', 
        projects.views.NominationDetailView.as_view(), 
        name='nomination_detail'),
    url(r'^project/(?P<project_id>\d+)/nominate/$', 
        projects.views.NominationCreateView.as_view(), 
        name='nominate'),
    url(r'^nominate/\*/(?P<url>.+)$', 
        projects.views.ResourceNominateView.as_view(),
        name='nominate_resource'),

    # Keyword
    url(r'^Keyword/(?P<pk>\d+)/$', 
        metadata.views.KeywordDetailView.as_view(),
        name = 'keyword_detail'),

    # Resource
    url(r'^resources/', include('webresources.urls')),

    # Auth
    url(r'^', include('django.contrib.auth.urls')),

    url(r'^ajax_select/', include(ajax_select_urls)),
    url(r'^admin/?', admin.site.urls),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns