# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-06 11:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import jsoneditor.forms


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', jsoneditor.forms.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='Writeup',
            fields=[
                ('slug', models.SlugField(primary_key=True, serialize=False)),
                ('writeup', models.TextField()),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Project')),
            ],
        ),
    ]
