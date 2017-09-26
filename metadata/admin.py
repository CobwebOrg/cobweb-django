from django.contrib import admin
from reversion.admin import VersionAdmin

from metadata.models import Keyword

# Register your models here.

@admin.register(Keyword)
class KeywordAdmin(VersionAdmin):
    pass