import django_tables2
import haystack
from dal import autocomplete
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as django_LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect, reverse
from django.utils.html import format_html
from django.views import generic
from haystack.generic_views import SearchView as HaystackGenericSearchView
from haystack.query import SearchQuerySet
from haystack.views import SearchView as HaystackWeirdSearchView
from reversion.views import RevisionMixin

from api.serializers import ResourceSerializer
from core import models
from core.forms import (LoginForm, SignUpForm, UserProfileForm,
                        OrganizationForm)
from core.tables import OrganizationTable, ResourceTable, UserTable
from projects.models import Project
from projects.tables import ClaimTable, NominationTable, ProjectTable, UserProjectsTable


class CobwebBaseIndexView(haystack.generic_views.SearchMixin,
                          django_tables2.SingleTableView):
    django_ct: str
    queryset = None
    template_name = 'generic_index.html'

    def get_queryset(self):
        if not self.queryset:
            self.queryset = (SearchQuerySet()
                             .filter(django_ct__exact=self.django_ct))
        return self.queryset


class FormMessageMixin(SuccessMessageMixin):

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        msg = format_html("Your submission could not be processed.")
        for error in form.non_field_errors():
            msg += format_html('<br>{}', error)
        for field, errors in form.errors.items():
            msg += format_html('<br>{}: {}', field, ' '.join(errors))
        # msg += format_html("</ul>")
        messages.error(self.request, msg)
        return super().form_invalid(form)

    def get_success_message(self, cleaned_data):
        verb = (     'created' if isinstance(self, generic.CreateView)
                else 'changed' if isinstance(self, generic.UpdateView)
                else 'saved')
        return f'Successfully {verb} {self.object._meta.verbose_name} {self.object}'


class DashboardView(LoginRequiredMixin,
                    django_tables2.SingleTableMixin,
                    generic.TemplateView):

    table_class = UserProjectsTable
    template_name = 'dashboard.html'

    def get_table_data(self):
        return Project.objects.filter(
            Q(administrators=self.request.user)
        )
    
    def get_table_kwargs(self):
        kwargs = super().get_table_kwargs()
        if self.request.user.is_authenticated:
            kwargs.update({'new_item_link': reverse('project_create')})
        return kwargs


class LoginView(django_LoginView):
    template_name = 'login.html'
    form_class = LoginForm


def get_landing_page_view(request):
    if request.user.is_authenticated:
        return DashboardView.as_view()(request)
    else:
        return LoginView.as_view()(request)


class UserIndexView(CobwebBaseIndexView):
    model = models.User
    table_class = UserTable
    django_ct = 'core.user'


class UserCreateView(FormMessageMixin, RevisionMixin, generic.CreateView):
    model = models.User
    template_name = "generic_form.html"
    form_class = SignUpForm


class UserUpdateView(LoginRequiredMixin, FormMessageMixin, RevisionMixin, generic.UpdateView):
    model = models.User
    template_name = "generic_form.html"
    form_class = UserProfileForm
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'editable': self.get_object() == self.request.user,
            'request': self.request,
        })
        return kwargs


class UserAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return models.User.objects.none()

        qs = models.User.objects.all()

        if self.q:
            qs = qs.filter(
                Q(username__icontains=self.q)
                | Q(first_name__icontains=self.q)
                | Q(last_name__icontains=self.q)
                | Q(email__icontains=self.q)
            )

        return qs


class OrganizationIndexView(CobwebBaseIndexView):
    model = models.Organization
    table_class = OrganizationTable
    django_ct = 'core.organization'

    def get_table_kwargs(self):
        kwargs = super().get_table_kwargs()
        if self.request.user.is_authenticated:
            kwargs.update({'new_item_link': reverse('organization_create')})
        return kwargs


class OrganizationCreateView(LoginRequiredMixin, FormMessageMixin, RevisionMixin,
                             generic.CreateView):
    model = models.Organization
    template_name = 'generic_form.html'
    form_class = OrganizationForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'editable': True,
            'request': self.request,
        })
        return kwargs


class OrganizationView(FormMessageMixin, RevisionMixin, generic.UpdateView):
    model = models.Organization
    template_name = 'generic_form.html'
    form_class = OrganizationForm
    slug_field = 'slug'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'editable': self.get_object().is_admin(self.request.user),
            'request': self.request,
        })
        return kwargs


class ResourceListView(CobwebBaseIndexView):
    model = models.Resource
    table_class = ResourceTable
    django_ct = 'core.resource'

    def get_queryset(self):
        result = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            result = result.filter(q=query)
        return result

    def get_context_data(self, **kwargs):
        """
        Get the context for this view.
        """

        context = super().get_context_data(**kwargs)
        try:
            searchbox_url = models.normalize_url(self.request.GET.get('q'))
            try:
                context['search_resource'] = (
                    models.Resource.objects.get(url=searchbox_url)
                )
            except models.Resource.DoesNotExist:
                context['search_resource'] = models.Resource(url=searchbox_url)
            except Exception as ex:
                raise ex
        except AttributeError:
            # No search query. That's fine.
            pass
        except ValidationError:
            # Search term isn't a url. That's fine.
            pass
        except Exception as ex:
            raise ex

        return context


class ResourceView(generic.DetailView):
    model = models.Resource
    template_name = "core/resource.html"

    def get(self, request, *args, **kwargs):
        """
        Overrides parent .get() method to perform URL normalization as
        follows:

        1. If url parameter is valid, invoke super().get(...)

        2. If url is valid but non-cannonical (i.e. url ~= normalize_url(url) )
        then return a redirect using the cannonical url.

        3. If url is not valid, return a 404

        Note that case #1 includes urls that are not yet in the database –
        custom logic for these cases in defined in .get_object(), which is
        invoked from the superclass's .get()
        """

        if 'url' in kwargs:
            try:
                normalized_url = models.normalize_url(kwargs['url'])
                if normalized_url != kwargs['url']:
                    return redirect(
                        reverse('resource', kwargs={'url': normalized_url})
                    )
            except ValidationError:
                raise Http404("{} is not a valid URL".format(kwargs['url']))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['react_data'] = {
            'user': self.request.user.username,
            'resource': ResourceSerializer(self.object).data,
        }
        return context

    def get_object(self, queryset=None):
        """
        Returns the Resource object for a url.

        If one doesn't exist, returns a new, unsaved Resource.
        """

        if queryset is None:
            queryset = self.get_queryset()

        try:
            obj = models.Resource.objects.get(url=self.kwargs['url'])
        except models.Resource.DoesNotExist:
            obj = models.Resource(url=self.kwargs['url'])

        return obj


class TagAutocomplete(autocomplete.Select2QuerySetView):

    create_field = 'title'

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return models.Tag.objects.none()

        qs = models.Tag.objects.all()
        if self.q:
            qs = qs.filter(title__istartswith=self.q)

        return qs

    def has_add_permission(self, request):
        """Return True if the user has the permission to add a model."""
        return request.user.is_authenticated


class SearchView(HaystackWeirdSearchView):
    pass
