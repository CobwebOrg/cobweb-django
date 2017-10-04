from ajax_select import make_ajax_form
from ajax_select.admin import AjaxSelectAdmin
from django.urls import reverse
from django.contrib import admin
from reversion.admin import VersionAdmin

from metadata.admin_inlines import MetadatumBaseInline

from projects.models import Nomination, Project
from projects.admin_inlines import NominationInline




class ProjectMDAdminInline(MetadatumBaseInline):
    model = Project.metadata.through


@admin.register(Project)
class ProjectAdmin(VersionAdmin, AjaxSelectAdmin):
    inlines = [ NominationInline ]
    # exclude = [ 'metadata' ]
    form = make_ajax_form(Project, {
        'administered_by': 'users',
        'metadata': 'metadata',
    })
    # filter_horizontal = [ 'administered_by' ]

@admin.register(Nomination)
class NominationAdmin(VersionAdmin):
    pass
