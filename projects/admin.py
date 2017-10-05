from ajax_select import make_ajax_form
from ajax_select.admin import AjaxSelectAdmin
from django.contrib import admin
from django.contrib.postgres import fields as postgres_fields
from django.urls import reverse
from django_json_widget.widgets import JSONEditorWidget
from reversion.admin import VersionAdmin

from projects.models import Nomination, Project
from projects.admin_inlines import NominationInline


@admin.register(Project)
class ProjectAdmin(VersionAdmin, AjaxSelectAdmin):
    inlines = [ NominationInline ]
    # form = make_ajax_form(Project, {
    #     'administered_by': 'users',
    # })
    filter_horizontal = [ 'administered_by' ]
    formfield_overrides = {
        postgres_fields.JSONField: {'widget': JSONEditorWidget},
    }

@admin.register(Nomination)
class NominationAdmin(VersionAdmin):
    pass
