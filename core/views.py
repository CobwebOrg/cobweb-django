import django_tables2
import haystack
from dal import autocomplete
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as django_LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect, reverse
from django.views import generic
from haystack.generic_views import SearchView as HaystackGenericSearchView
from haystack.views import SearchView as HaystackWeirdSearchView
from haystack.query import SearchQuerySet
from reversion.views import RevisionMixin

from core import models
from core.forms import LoginForm, SignUpForm, UserProfileForm
from core.tables import OrganizationTable, ResourceTable, UserTable
from projects.tables import ClaimTable, NominationTable, ProjectTable


class CobwebBaseIndexView(haystack.generic_views.SearchMixin,
                          django_tables2.SingleTableView):
    template_name = 'generic_index.html'
    queryset = None

    def get_queryset(self):
        if not self.queryset:
            self.queryset = (SearchQuerySet()
                             .filter(django_ct__exact=self.django_ct))
        return self.queryset


class FormMessageMixin(SuccessMessageMixin):

    success_message = "%(title)s saved successfully"

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        msg = format_html("Your submission could not be processed.<ul>")
        for error in form.non_field_errors():
            msg += format_html('<li>{}</li>', error)
        for field, error in form.errors.items():
            msg += format_html('<li>{}: {}</li>', field, error)
        msg += format_html("</ul>")
        messages.add_message(self.request, messages.ERROR, msg)
        return super().form_invalid(form)


class DashboardView(LoginRequiredMixin,
                    django_tables2.MultiTableMixin,
                    generic.TemplateView):

    template_name = 'dashboard.html'

    def get_tables(self):
        # TODO: filter by user
        user = self.request.user
        return (
            ProjectTable(
                data=SearchQuerySet().filter(django_ct__exact='projects.project'),
                table_title='my projects',
            ),
            NominationTable(
                data=SearchQuerySet().filter(django_ct__exact='projects.nomination'),
                table_title='my nominations',
            ),
            ClaimTable(
                data=SearchQuerySet().filter(django_ct__exact='projects.claim'),
                table_title='my claims and holdings',
            ),
        )


class LoginView(django_LoginView):
    template_name='login.html'
    form_class=LoginForm


def get_landing_page_view(request):
    if request.user.is_authenticated:
        return DashboardView.as_view()(request)
    else:
        return LoginView.as_view()(request)


class UserIndexView(CobwebBaseIndexView):
    model = models.User
    table_class = UserTable
    django_ct = 'core.user'



class UserCreateView(RevisionMixin, generic.CreateView):
    model = models.User
    template_name = "generic_form.html"
    form_class = SignUpForm


class UserUpdateView(RevisionMixin, generic.UpdateView):
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
            'editable': self.get_object() == self.request.user
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

class OrganizationDetailView(generic.DetailView):
    model = models.Organization


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
    section = 'resource'

    def get(self, request, *args, **kwargs):
        """
        Overrides parent .get() method to perform URL normalization as
        follows:

        1. If url parameter is valid, or if called w/ id/pk instead of url,
        invoke super().get(...)

        2. If url is valid but non-cannonical (i.e. url ~= normalize_url(url) )
        then return a redirect using the cannonical url.

        3. If url is not valid, return a 404 or something [not implemented yet]

        Note that case #1 includes urls that are not yet in the database –
        custom logic for these cases in defined in .get_object(), which is
        invoked from the superclass's .get()
        """

        if 'url' in kwargs:
            try:
                normalized_url = models.normalize_url(kwargs['url'])
                if normalized_url != kwargs['url']:
                    return redirect(
                        reverse(
                            'resource',
                            kwargs={'url': normalized_url}
                        )
                    )
            except ValidationError:
                raise Http404("{} is not a valid URL".format(kwargs['url']))
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        """
        Returns the object the view is displaying.
        Overrides DetailView.get_object using a `url` argument from the URLconf
        to find a Resource object. If no `url` argument is found, calls
        super().get_object(...), which tries with `pk` or `slug`.

        If a url is provided but no matching resource is in the database,
        returns a new, unsaved object. This allows the ResourceView to
        provide information such as parent/child resources, along with forms
        for nominating/claiming it (in which case the Resource should be saved
        along w/ Nomination or Claim object).
        """

        # Use a custom queryset if provided; this is required for subclasses
        # like DateDetailView
        if queryset is None:
            queryset = self.get_queryset()
        url = self.kwargs.get('url')
        if url is not None:
            try:
                obj = models.Resource.objects.get(url=url)
            except queryset.model.DoesNotExist:
                obj = models.Resource(url=url)
            except Exception as ex:
                raise ex
        else:
            obj = super().get_object(queryset)

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

    # def get_queryset(self, *args, **kwargs):
    #     q = self.request.GET.get('q')
    #     qs = SearchQuerySet().filter(content__fuzzy=q)
    #     qs.order_by('impact_factor')
    #     return qs
