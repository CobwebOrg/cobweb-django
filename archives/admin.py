from django.urls import reverse
from django.contrib import admin
from reversion.admin import VersionAdmin

from metadata.admin import MetadataAdminMixin
from projects.admin_inlines import ClaimInline

from archives import models, admin_inlines


@admin.register(models.Collection)
class CollectionAdmin(MetadataAdminMixin, VersionAdmin):
    fields = ['title', 'administrators', 'organization', 'identifier'] + MetadataAdminMixin.fields
    inlines = [
        ClaimInline,
        admin_inlines.HoldingInline,
    ]


@admin.register(models.Holding)
class HoldingAdmin(VersionAdmin):
    readonly_fields = ['resource_link']

    def resource_link(self, instance):
        if instance.id:
            changeform_url = reverse('admin:webresources_resource_change',
                                     args=(instance.resource.id,))
            return (
                '<a href="{changeform_url}" target="_blank">{resource}</a>'
                .format(
                    changeform_url=changeform_url,
                    resource=instance.resource,
                )
            )
        else:
            return u''
    resource_link.allow_tags = True
    resource_link.short_description = 'Resource'

    fields = [
        'resource_link',
        'collection',
        'description',
        'keywords',
        'metadata',
    ]
