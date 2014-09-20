# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Departments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='employee',
            name='dept',
            field=models.ForeignKey(to='leave.Departments'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='dept',
            field=models.ForeignKey(to='leave.Departments'),
        ),
    ]
