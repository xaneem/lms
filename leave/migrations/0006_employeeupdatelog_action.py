# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0005_auto_20140927_2257'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeeupdatelog',
            name='action',
            field=models.ForeignKey(default=1, to='leave.Action'),
            preserve_default=False,
        ),
    ]
