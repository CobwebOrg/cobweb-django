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

    url(r'^$', core.views.DashboardView.as_view(), name='dashboard',),

    # Auth: /login, /logout, /password_change, /password_reset, /reset
    path('accounts/login/', auth.views.LoginView.as_view(
        template_name='login.html',
        form_class=core.forms.LoginForm
    ), name='login',),
    path('', include('django.contrib.auth.urls')),

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
    path('p/projects',
        projects.views.ProjectIndexView.as_view(),
        name='project_list'),
    path('p/<int:pk>',
        projects.views.ProjectSummaryView.as_view(),
        name='project_summary'),
    path('p/<int:pk>/nominations',
        projects.views.ProjectNominationsView.as_view(),
        name='project_nominations'),
    path('p/new',
        projects.views.ProjectCreateView.as_view(),
        name='project_create'),

    # Nomination
    path('nomination/<int:pk>',
        projects.views.NominationView.as_view(),
        name='nomination'),
    path('p/<int:project_id>/nominate',
        projects.views.NominationCreateView.as_view(),
        name='project_nominate'),
    path('nominate/<path:url>',
        projects.views.ResourceNominateView.as_view(),
        name='nominate_resource'),

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

    # Collection
    url(r'^collections/', include('archives.urls')),

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

    path('admin', admin.site.urls),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
