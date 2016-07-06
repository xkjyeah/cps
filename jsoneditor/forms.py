from django.forms.widgets import Textarea
from django.forms.utils import flatatt
from django.utils.safestring import mark_safe
from django.conf import settings
from django.db.models import Field, TextField
from django import forms

import json

class JSONEditor(Textarea):
    class Media:
        js = (
            settings.STATIC_URL + 'jsoneditor/jsoneditor.min.js',
            settings.STATIC_URL + 'jsoneditor/mount.js',
        )
        # css= {'all': (getattr(settings, "JSON_EDITOR_CSS",settings.STATIC_URL+'jsoneditor/jsoneditor.css'),)}
        css = {
            'all': ('https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css',)
        }

    def __init__(self, schema=None, *args, **kwargs):
        self.schema = schema
        super(Textarea, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        print(value)
        if not isinstance(value, str):
           value = json.dumps(value)

        # Get the schema
        schema = self.schema

        # Make the text area hidden
        input_attrs = {'hidden':True}
        input_attrs.update(attrs)
        if not 'class' in input_attrs:
            input_attrs['class'] = 'for_jsoneditor'
        else:
            input_attrs['class'] += ' for_jsoneditor'

        # Add the div
        r = super(JSONEditor,self).render(name, value, input_attrs)
        div_attrs = dict()
        div_attrs.update(attrs)
        div_attrs.update({
            "id": attrs['id']+'_jsoneditor',
            'data-schema': json.dumps(schema),
            'class': attrs.get('class', '') + ' for_jsoneditor',
        })

        final_attrs = self.build_attrs(div_attrs, name=name)
        r += '''
        <div %(attrs)s></div>
        ''' % {
            'attrs':flatatt(final_attrs),
        }
        return mark_safe(r)

class JSONFormField(forms.CharField):
    def __init__(self, schema=None, *args, **kwargs):
        self.schema = schema
        self.max_length = None
        kwargs['widget'] = JSONEditor(schema=self.schema)
        super(forms.CharField, self).__init__(*args, **kwargs)

    def clean(self, value):
        json.loads(value)
        return value

    def to_python(self, value):
        return value

class JSONField(TextField):
    def __init__(self, *args, schema=None, **kwargs):
        self.schema = schema
        super(TextField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            # 'max_length': None,
            'form_class': kwargs.get('form_class', JSONFormField),
            'schema': self.schema
        }
        defaults.update(kwargs)
        return super(TextField, self).formfield(**defaults)

    def deconstruct(self):
        name, path, args, kwargs = super(HandField, self).deconstruct()
        kwargs['schema'] = self.schema
        return name, path, args, kwargs

    def __str__(self):
        return self.name

    def from_db_value(self, value, expression, connection, context):
        # Always return schema
        return json.loads(value)

    def to_python(self, value):
        return json.loads(value)

    def get_prep_value(self, value):
        return json.dumps(value)
