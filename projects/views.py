from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from projects import models, forms



class FormsetMixin(object):
    object = None

    def get(self, request, *args, **kwargs):
        if getattr(self, 'is_update_view', False):
            self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset_class = self.get_formset_class()
        formset = self.get_formset(formset_class)
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def post(self, request, *args, **kwargs):
        if getattr(self, 'is_update_view', False):
            self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset_class = self.get_formset_class()
        formset = self.get_formset(formset_class)
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def get_formset_class(self):
        return self.formset_class

    def get_formset(self, formset_class):
        return formset_class(**self.get_formset_kwargs())

    def get_formset_kwargs(self):
        kwargs = {
            'instance': self.object
        }
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def form_valid(self, form, formset):
        self.object = form.save()
        formset.instance = self.object
        formset.save()
        return redirect(self.object.get_absolute_url())

    def form_invalid(self, form, formset):
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

class ProjectIndexView(ListView):
    model = models.Project
    template_name = "project_list.html"

class ProjectDetailView(DetailView):
    model = models.Project
    template_name = "project_detail.html"

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = models.Project
    template_name = 'generic_form.html'
    form_class = forms.ProjectForm

    # def form_valid(self, form):
    #     candidate = form.save(commit=False)
    #     candidate.administered_by.add(self.request.user)

    #     candidate.save()
    #     return super().form_valid(form)

class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Project
    template_name = 'generic_form.html'
    form_class = forms.ProjectForm
    # formset_class = forms.ProjectMDInlineFormset

class NominationDetailView(DetailView):
    model = models.Nomination
    template_name = 'nomination_detail.html'

class NominationCreateView(CreateView):
    model = models.Nomination
    template_name = 'generic_form.html'
    form_class = forms.NominationForm

    def form_valid(self, form):
        print(self.request.path)
        print(self.kwargs)
        candidate = form.save(commit=False)
        candidate.project = models.Project.objects.get(pk=self.kwargs['project_id'])
        self.success_url = candidate.project.get_absolute_url()
        candidate.nominated_by = self.request.user
        candidate.save()
        return super().form_valid(form)