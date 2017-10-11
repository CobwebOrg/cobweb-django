# from reversion.views import RevisionMixin
# from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import generic

from webresources import models



class ResourceIndexView(generic.ListView):
    model = models.Resource
    template_name = "webresources/resource_list.html"

class ResourceDetailView(generic.DetailView):
    model = models.Resource
    template_name = "webresources/resource.html"

# class ResourceCreateView(LoginRequiredMixin, RevisionMixin, generic.CreateView):
#     model = models.Resource
#     template_name = 'generic_form.html'
#     form_class = forms.ResourceForm

#     # def form_valid(self, form):
#     #     candidate = form.save(commit=False)
#     #     candidate.administered_by.add(self.request.user)

#     #     candidate.save()
#     #     return super().form_valid(form)

# class ResourceUpdateView(UserPassesTestMixin, RevisionMixin, generic.UpdateView):
#     model = models.Resource
#     template_name = 'generic_form.html'
#     form_class = forms.ResourceForm
#     # formset_class = forms.ResourceMDInlineFormset

#     def test_func(self):
#         return self.get_object().is_admin(self.request.user)