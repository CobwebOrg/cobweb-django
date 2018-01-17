from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.views.generic import DetailView, CreateView, UpdateView
import django_tables2
from django_tables2.utils import Accessor
from reversion.views import RevisionMixin

from webresources.models import Resource

from projects import models, forms


class ProjectTable(django_tables2.Table):
    """django_tables2.Table object for lists of projects."""

    title = django_tables2.LinkColumn()
    nholdings = django_tables2.TemplateColumn(
        '{% load resource_count_badge from cobweb_look %}'
        '{% resource_count_badge record %}',
        default='', orderable=False
    )

    class Meta:
        model = models.Project
        show_header = False
        fields = ['title', 'nholdings']
        # attrs = {'class': 'table table-hover'}
        empty_text = "No projects."


class NominationTable(django_tables2.Table):
    """django_tables2.Table object for lists of projects."""

    resource = django_tables2.LinkColumn(
        'webresources:detail',
        kwargs={'url': Accessor('resource.url')}
    )
    keywords = django_tables2.TemplateColumn(
        """
        {% load badge from cobweb_look %}
        <small>
            {% for keyword in record.keywords.all %}
                {% badge keyword %}
            {% endfor %}
        </small>
        """, default='', orderable=False
    )

    class Meta:
        model = models.Project
        show_header = False
        fields = []
        # attrs = {'class': 'table table-hover'}
        empty_text = "No nominations."


class ProjectIndexView(django_tables2.SingleTableView):
    model = models.Project
    template_name = "generic_index.html"
    table_class = ProjectTable

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context_data.update({
                'new_item_link': reverse('project_create'),
            })
        return context_data


class ProjectDetailView(django_tables2.SingleTableMixin, DetailView):
    model = models.Project
    template_name = "project.html"
    table_class = NominationTable

    def get_table_data(self):
        return self.object.nominations.all()


class ProjectCreateView(LoginRequiredMixin, RevisionMixin, CreateView):
    model = models.Project
    template_name = 'generic_form.html'
    form_class = forms.ProjectForm

    def get_initial(self):
        initial = super().get_initial()
        initial['administrators'] = {self.request.user.pk}
        print(initial)
        return initial

    # def form_valid(self, form):
    #     candidate = form.save(commit=False)
    #     candidate.administrators.add(self.request.user)

    #     candidate.save()
    #     return super().form_valid(form)


class ProjectUpdateView(UserPassesTestMixin, RevisionMixin, UpdateView):
    model = models.Project
    template_name = 'generic_form.html'
    form_class = forms.ProjectForm

    def test_func(self):
        return self.get_object().is_admin(self.request.user)


class NominationDetailView(DetailView):
    model = models.Nomination
    template_name = 'nomination_detail.html'


class NominationCreateView(UserPassesTestMixin, RevisionMixin, CreateView):
    model = models.Nomination
    template_name = 'generic_form.html'
    form_class = forms.NominateToProjectForm

    def form_valid(self, form):
        print(self.request.path)
        print(self.kwargs)
        candidate = form.save(commit=False)
        candidate.project = self.get_project()
        self.success_url = candidate.project.get_absolute_url()
        candidate.nominated_by.add(self.request.user)
        candidate.save()
        return super().form_valid(form)

    def get_initial(self):
        return {
            'nominated_by': [self.request.user],
            'project': self.get_project(),
        }

    def get_project(self):
        return models.Project.objects.get(pk=self.kwargs['project_id'])

    def test_func(self):
        return self.get_project().is_nominator(self.request.user)


class ResourceNominateView(RevisionMixin, CreateView):
    model = models.Nomination
    template_name = 'generic_form.html'
    form_class = forms.ResourceNominateForm

    def form_valid(self, form):
        print(self.request.path)
        print(self.kwargs)
        candidate = form.save(commit=False)
        candidate.resource = self.get_resource()
        self.success_url = candidate.resource.get_absolute_url()
        candidate.nominated_by = self.request.user
        candidate.save()
        return super().form_valid(form)

    def get_initial(self):
        return {
            'nominated_by': [self.request.user],
            'resource': self.kwargs['url'],
        }

    def get_resource(self):
        try:
            obj = Resource.objects.get(url=self.kwargs['url'])
        except Resource.DoesNotExist:
            obj = Resource(url=self.kwargs['url'])
        except Exception as ex:
            raise ex

        return obj

    def test_func(self):
        return True
        # return self.get_project().is_nominator(self.request.user)
