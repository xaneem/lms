# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0006_employeeupdatelog_action'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeupdatelog',
            name='action',
            field=models.ForeignKey(related_name=b'update_log', to='leave.Action'),
        ),
    ]
