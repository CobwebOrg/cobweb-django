from dal import autocomplete
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.views import generic
from reversion.views import RevisionMixin

from core.forms import UserForm


class UserIndexView(generic.ListView):
    model = get_user_model()
    template_name = "user_list.html"


class UserDetailView(generic.DetailView):
    model = get_user_model()
    template_name = "user_detail.html"


class UserCreateView(RevisionMixin, generic.CreateView):
    model = get_user_model()
    template_name = "generic_form.html"
    form_class = UserForm


class UserUpdateView(RevisionMixin, generic.UpdateView):
    model = get_user_model()
    template_name = "generic_form.html"
    form_class = UserForm


class UserAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return get_user_model().objects.none()

        qs = get_user_model().objects.all()

        if self.q:
            qs = qs.filter(
                  Q(username__icontains=self.q)
                | Q(first_name__icontains=self.q)
                | Q(last_name__icontains=self.q)
                | Q(email__icontains=self.q)
            )

        return qs
