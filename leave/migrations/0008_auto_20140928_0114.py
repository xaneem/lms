# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0007_auto_20140928_0113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeupdatelog',
            name='action',
            field=models.OneToOneField(related_name=b'update_log', to='leave.Action'),
        ),
    ]
