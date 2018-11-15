import haystack
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin, auth
from django.urls import path
from django.views.generic import FormView, DetailView, TemplateView
from rest_framework import viewsets
from rest_framework.routers import DefaultRouter

from api import serializers
from api.views import (UserViewSet, OrganizationViewSet, ResourceViewSet,
                       ProjectViewSet, NominationViewSet, ClaimViewSet)
import core.forms
import core.views
import projects.views
import projects.models
import webarchives.models
from jargon.terms import TERMS


router = DefaultRouter()

router.register(r'users', UserViewSet)
router.register(r'organizations', OrganizationViewSet)

router.register(r'resources', ResourceViewSet)

router.register(r'projects', ProjectViewSet)
router.register(r'nominations', NominationViewSet)
router.register(r'claims', ClaimViewSet)

class TestViewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.ArchiveResourceSerializer
    queryset = webarchives.models.ImportedRecord.objects.filter(record_type='resource')
router.register(r'test', TestViewset)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('search/',
         haystack.views.SearchView(form_class=core.forms.SearchForm),
         name='search'),

    path('', core.views.get_landing_page_view, name='landing_page'),

    path('dashboard', core.views.DashboardView.as_view(), name='dashboard'),

    # Auth: /login, /logout, /password_change, /password_reset, /reset
    path('accounts/login/', core.views.LoginView.as_view(), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),

    # User
    path('user_list',
         core.views.UserIndexView.as_view(),
         name='user_list'),
    path('user_create',
         core.views.UserCreateView.as_view(),
         name='user_create'),
    path('user/<slug:username>',
         core.views.UserUpdateView.as_view(),
         name='user'),
    path('user_delete/<slug:username>',
         core.views.UserDeleteView.as_view(),
         name='user_delete'),
    path('user_autocomplete',
         core.views.UserAutocomplete.as_view(),
         name='user_autocomplete'),

    # Organization
    path('org/',
         core.views.OrganizationIndexView.as_view(),
         name='organization_list'),
    path('org_create',
         core.views.OrganizationCreateView.as_view(),
         name='organization_create'),
    path('org/<slug:slug>',
         core.views.OrganizationView.as_view(),
         name='organization'),
    path('org_delete/<slug:slug>',
         core.views.OrganizationDeleteView.as_view(),
         name='organization_delete'),

    # Project
    path('proj/',
         projects.views.ProjectIndexView.as_view(),
         name='project_list'),
    path('proj_create',
         projects.views.ProjectCreateView.as_view(),
         name='project_create'),
    path('proj/<slug:slug>',
         projects.views.ProjectView.as_view(),
         name='project'),
    path('proj_delete/<slug:slug>',
         projects.views.ProjectDeleteView.as_view(),
         name='project_delete'),

    # Nomination
    path('proj/<slug:project_slug>/nominate',
         projects.views.NominationCreateView.as_view(),
         name='nomination_create'),
    path('proj/<slug:project_slug>/<path:url>',
         projects.views.NominationUpdateView.as_view(),
         name='nomination_update'),
    path('nom_delete/<slug:project_slug>/<path:url>',
         projects.views.NominationDeleteView.as_view(),
         name='nomination_delete'),

    # Claim
    path('nomination/<int:nomination_pk>/claim',
         projects.views.ClaimCreateView.as_view(),
         name='claim_create'),
    path('claim/<int:pk>',
         projects.views.ClaimUpdateView.as_view(),
         name='claim'),
    path('claim_delete/<int:pk>',
         projects.views.ClaimDeleteView.as_view(),
         name='claim_delete'),

    # Tags
    # path('tags/<int:pk>/',
    #      core.views.TagDetailView.as_view(),
    #      name='tag_detail'),
    path('tags/autocomplete/',
         core.views.TagAutocomplete.as_view(create_field='title'),
         name='tag_autocomplete'),

    # Resource
    path('url/', core.views.ResourceListView.as_view(), name='resource_list'),
    path('url/<path:url>', core.views.ResourceView.as_view(), name='resource'),

    path('glossary',
         TemplateView.as_view(
             template_name='glossary.html',
             extra_context={'terms': TERMS}
         ),
         name='glossary'),
    path('about_cobweb',
         TemplateView.as_view(template_name='static_pages/static_page.html',
                              extra_context={'text': 'static_pages/about_cobweb.html'}),
         name='about_cobweb'),
    path('getting_started',
         TemplateView.as_view(template_name='static_pages/static_page.html',
                              extra_context={'text': 'static_pages/getting_started.html'}),
         name='getting_started'),
    path('terms_of_use',
         TemplateView.as_view(template_name='static_pages/static_page.html',
                              extra_context={'text': 'static_pages/terms_of_use.html'}),
         name='terms_of_use'),

    path('admin', admin.site.urls),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
