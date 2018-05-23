from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin, auth
from django.urls import path
from django.views.generic import FormView
from rest_framework.routers import DefaultRouter

from api.views import (UserViewSet, OrganizationViewSet, ProjectViewSet,
                       NominationViewSet, ClaimViewSet)
# import archives.views
import core.forms
import core.views
import projects.views


router = DefaultRouter()

router.register(r'users', UserViewSet)
router.register(r'organizations', OrganizationViewSet)

router.register(r'projects', ProjectViewSet)
router.register(r'nominations', NominationViewSet)
router.register(r'claims', ClaimViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^search/', core.views.SearchView.as_view(), name='search'),

    url(r'^$', auth.views.LoginView.as_view(
        template_name='landing_page.html',
        form_class=core.forms.LoginForm
    ), name='front_page',),

    # User
    path('users/<pk>/edit/',
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
    
    # Organization
    path('organizations/',
         core.views.OrganizationIndexView.as_view(),
         name='organization_list'),

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
    url(r'^projects/(?P<pk>\d+)/edit$',
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
    path('nomination/<int:pk>/edit',
         projects.views.NominationUpdateView.as_view(),
         name='nomination_update'),

    # Claim
    path('claim/<int:pk>',
         projects.views.ClaimDetailView.as_view(),
         name='claim_detail'),
    path('nomination/<int:nomination_pk>/claim',
         projects.views.ClaimCreateView.as_view(),
         name='claim_create'),
    path('claim/<int:pk>/edit',
         projects.views.ClaimUpdateView.as_view(),
         name='claim_update'),

    # Tags
    # path('tags/<int:pk>/',
    #      core.views.TagDetailView.as_view(),
    #      name='tag_detail'),
    path('tags/autocomplete/',
         core.views.TagAutocomplete.as_view(create_field='name'),
         name='tag_autocomplete'),

    # Resource
    path('resources/', core.views.ResourceListView.as_view(), name='resource_list'),
    path('resources/<path:url>', core.views.ResourceDetailView.as_view(), name='resource_detail'),

    # Auth
    url(r'^accounts/', include('django.contrib.auth.urls')),

    path('admin', admin.site.urls),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
