# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0008_auto_20140928_0114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
