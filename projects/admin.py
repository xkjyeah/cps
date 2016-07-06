from django.contrib import admin
from .models import Project, Writeup
from jsoneditor.forms import JSONEditor, JSONField

# Register your models here.
class WriteupInline(admin.TabularInline):
    model = Writeup
    extra = 1

class ProjectAdmin(admin.ModelAdmin):
    inlines = [WriteupInline]
    formfield_overrides = {
        JSONField: {
            'widget': JSONEditor
        }
    }


admin.site.register(Project, ProjectAdmin)
