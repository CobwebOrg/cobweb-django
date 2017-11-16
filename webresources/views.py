import django_tables2 as tables

from django.core.exceptions import ValidationError
from django.http import Http404
from django.views import generic
from django.shortcuts import redirect, reverse

from webresources import models


class ResourceTable(tables.Table):

    url = tables.Column()
    n = tables.TemplateColumn('{{record.nominations.count}}', orderable=False)
    c = tables.TemplateColumn('{{record.claims.count}}', orderable=False)
    h = tables.TemplateColumn('{{record.holdings.count}}', orderable=False)
    # records = tables.TemplateColumn('{{record.resource_record_count}}',
    #                                 orderable=False)

    class Meta:
        model = models.Resource
        show_header = True
        exclude = ['id']
        attrs = {'class': 'table table-hover'}
        template = 'webresources/resource-table.html'
        empty_text = "No records."


class ResourceListView(tables.SingleTableView):
    model = models.Resource
    template_name = "webresources/resource_list.html"
    table_class = ResourceTable

    def get_queryset(self):
        result = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            result = result.filter(url__icontains=query)
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


class ResourceDetailView(generic.DetailView):
    model = models.Resource
    template_name = "webresources/resource.html"

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
                            'webresources:detail',
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
        returns a new, unsaved object. This allows the ResourceDetailView to
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
