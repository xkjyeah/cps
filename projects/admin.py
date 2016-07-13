from django.contrib import admin
from .models import Project, Writeup, Organization
from jsoneditor.forms import JSONEditor, JSONField

# Register your models here.
class OrganizationAdmin(admin.ModelAdmin):
    model = Organization
    list_display = ('name',)
    formfield_overrides = {
        JSONField: {
            'widget': JSONEditor
        }
    }

class ProjectAdmin(admin.ModelAdmin):
    formfield_overrides = {
        JSONField: {
            'widget': JSONEditor
        }
    }


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Project, ProjectAdmin)
