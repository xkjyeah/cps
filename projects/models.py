from django.db import models
from jsoneditor.forms import JSONField

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=100)
    description = JSONField(schema={
        "type": "object",
        "title": "Person",
        "properties": {
            "name": {
                "type": "string"
            },
            "address": {
                "type": "string"
            },
        }
    })

    def __str__(self):
        return self.name

class Writeup(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    slug = models.SlugField(primary_key=True)
    writeup = models.TextField()

    def __str__(self):
        return self.slug if self.slug else '(null)'
