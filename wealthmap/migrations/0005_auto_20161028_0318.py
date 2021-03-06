# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-28 03:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wealthmap', '0004_remove_opportunitysearch_benefit_types'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opportunity',
            name='existing_business',
            field=models.CharField(blank=True, choices=[('existing', 'existing business'), ('new', 'new business'), ('', 'either')], max_length=8, null=True, verbose_name='this opportunity applies to'),
        ),
        migrations.AlterField(
            model_name='opportunity',
            name='small_business',
            field=models.BooleanField(verbose_name='must be a small business'),
        ),
        migrations.AlterField(
            model_name='opportunitysearch',
            name='existing_business',
            field=models.CharField(blank=True, choices=[('existing', 'existing business'), ('new', 'new business'), ('', 'either')], max_length=8, null=True, verbose_name='existing business'),
        ),
    ]
