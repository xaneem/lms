# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0004_auto_20140923_1828'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeUpdateLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_new', models.BooleanField(default=False)),
                ('new_name', models.CharField(max_length=100)),
                ('new_email', models.EmailField(max_length=75)),
                ('new_is_active', models.BooleanField(default=True)),
                ('old_name', models.CharField(max_length=100)),
                ('old_email', models.EmailField(max_length=75)),
                ('old_is_active', models.BooleanField(default=True)),
                ('employee', models.ForeignKey(to='leave.Employee')),
                ('new_dept', models.ForeignKey(related_name=b'update_new_dept', to='leave.Department')),
                ('old_dept', models.ForeignKey(related_name=b'update_old_dept', to='leave.Department')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='action',
            name='is_leave',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
