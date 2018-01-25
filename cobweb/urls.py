from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path

# import archives.views
import core.views
import projects.views
import metadata.views

# from metadata.models import Keyword


urlpatterns = [
    url(r'^search/', include('haystack.urls')),

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

    # Collection
    url(r'^collections/', include('archives.urls')),

    # Nomination
    url(r'^nomination/(?P<pk>\d+)/$',
        projects.views.NominationDetailView.as_view(),
        name='nomination_detail'),
    url(r'^project/(?P<project_id>\d+)/nominate/$',
        projects.views.NominationCreateView.as_view(),
        name='nominate'),
    url(r'^nominate/(?P<url>.+)$',
        projects.views.ResourceNominateView.as_view(),
        name='nominate_resource'),

    # Claim
    path('nomination/<int:nomination_pk>/claim',
         projects.views.ClaimCreateView.as_view(),
         name='claim'),

    # Keyword
    url(r'^Keyword/(?P<pk>\d+)/$',
        metadata.views.KeywordDetailView.as_view(),
        name='keyword_detail'),
    url(r'^keywords/autocomplete/$',
        metadata.views.KeywordAutocomplete.as_view(create_field='name'),
        name='keyword_autocomplete'),

    # Resource
    url(r'^resources/', include('webresources.urls')),

    # Auth
    url(r'^accounts/', include('django.contrib.auth.urls')),

    url(r'^admin/?', admin.site.urls),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
