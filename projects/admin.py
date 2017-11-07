from django.contrib import admin
from django.contrib.postgres import fields as postgres_fields
from django.urls import reverse
from django_json_widget.widgets import JSONEditorWidget
from reversion.admin import VersionAdmin

from projects.models import Nomination, Project
from projects.admin_inlines import NominationInline


@admin.register(Project)
class ProjectAdmin(VersionAdmin):
    inlines = [ NominationInline ]
    filter_horizontal = [ 'keywords', 'administered_by', 'nominators' ]
    formfield_overrides = {
        postgres_fields.JSONField: {'widget': JSONEditorWidget},
    }

@admin.register(Nomination)
class NominationAdmin(VersionAdmin):
    pass
