# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import leave.CustomFileField


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0003_auto_20140921_0023'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='post',
        ),
        migrations.AlterField(
            model_name='application',
            name='attachment1',
            field=leave.CustomFileField.CustomFileField(null=True, upload_to=b'.', blank=True),
        ),
        migrations.AlterField(
            model_name='application',
            name='attachment2',
            field=leave.CustomFileField.CustomFileField(null=True, upload_to=b'.', blank=True),
        ),
        migrations.AlterField(
            model_name='application',
            name='attachment3',
            field=leave.CustomFileField.CustomFileField(null=True, upload_to=b'.', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user_type',
            field=models.IntegerField(choices=[(0, b''), (1, b'Section Head'), (2, b'Est. Office'), (4, b'Deputy Registrar'), (5, b'Data Admin')]),
        ),
    ]
