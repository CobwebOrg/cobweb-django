from dal import autocomplete
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.forms import ModelForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, RedirectView

import archives.views, core.views, projects.views, metadata.views

from metadata.models import Keyword


urlpatterns = [
    url(r'^$', projects.views.ProjectIndexView.as_view(), name='front_page'),
    
    # User
    url(r'^users/(?P<pk>\d+)/edit/$', 
        core.views.UserUpdateView.as_view(), 
        name='user_update'),
    url(r'^users/(?P<pk>\d+)/$', 
        core.views.UserDetailView.as_view(), 
        name='user_detail'),
    url(r'^users/new$', 
        core.views.UserCreateView.as_view(), 
        name='user_create'),
    url(r'^users/$', 
        core.views.UserIndexView.as_view(), 
        name='user_list'),
    url(r'^users/autocomplete/$', 
        core.views.UserAutocomplete.as_view(), 
        name='user_autocomplete'),

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

    # # Collection
    # url(r'^collections/$', 
    #     archives.views.CollectionIndexView.as_view(),
    #     name='collection_list'),
    # url(r'^collections/(?P<pk>\d+)/$', 
    #     archives.views.CollectionDetailView.as_view(),
    #     name='collection_detail'),
    # url(r'^collections/new$', 
    #     archives.views.CollectionCreateView.as_view(),
    #     name='collection_create'),
    # url(r'^collections/(?P<pk>\d+)/edit/$', 
    #     archives.views.CollectionUpdateView.as_view(), 
    #     name='collection_update'),
    
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
    url(r'^keywords/autocomplete/$', 
        # autocomplete.Select2QuerySetView.as_view(model=Keyword, create_field='name'),
        metadata.views.KeywordAutocomplete.as_view(create_field='name'), 
        name='keyword_autocomplete'),

    # Resource
    url(r'^resources/', include('webresources.urls')),

    # Auth
    url(r'^', include('django.contrib.auth.urls')),

    url(r'^admin/?', admin.site.urls),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns