# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count', models.IntegerField(default=0)),
                ('note', models.TextField(max_length=100, null=True, blank=True)),
                ('status', models.IntegerField(default=1, choices=[(0, b'Deleted'), (1, b'Pending'), (2, b'Processing'), (3, b'Approved'), (4, b'Rejected'), (5, b'Cancelled')])),
                ('time_generated', models.DateTimeField(auto_now_add=True)),
                ('time_approved', models.DateTimeField(null=True)),
                ('reply_note', models.TextField(max_length=100, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_new', models.BooleanField(default=True)),
                ('is_credit', models.BooleanField(default=False)),
                ('leave_type', models.IntegerField(choices=[(1, b'Earned Leave'), (2, b'Half Pay Leave'), (3, b'Commuted Leave')])),
                ('date_from', models.DateField(null=True)),
                ('date_to', models.DateField(null=True)),
                ('days', models.IntegerField(default=0)),
                ('status', models.IntegerField(default=1, choices=[(0, b'Deleted'), (1, b'Pending'), (2, b'Processing'), (3, b'Approved'), (4, b'Rejected'), (5, b'Cancelled')])),
                ('reason', models.TextField(max_length=200)),
                ('new_date_to', models.DateField(null=True)),
                ('new_date_from', models.DateField(null=True)),
                ('attachment1', models.FileField(null=True, upload_to=b'.', blank=True)),
                ('attachment2', models.FileField(null=True, upload_to=b'.', blank=True)),
                ('attachment3', models.FileField(null=True, upload_to=b'.', blank=True)),
                ('time_generated', models.DateTimeField(auto_now_add=True)),
                ('time_received', models.DateTimeField(null=True)),
                ('time_approved', models.DateTimeField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ApplicationLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField()),
                ('activity', models.TextField(max_length=100, null=True, blank=True)),
                ('notes', models.TextField(max_length=100, null=True, blank=True)),
                ('application', models.ForeignKey(to='leave.Application')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=10, unique=True, null=True)),
                ('name', models.CharField(max_length=100)),
                ('dept', models.IntegerField(choices=[(0, b'Other'), (1, b'Computer Science'), (2, b'Mechanical'), (3, b'Electrical'), (4, b'Civil'), (5, b'Electronics'), (6, b'Chemical'), (7, b'Biotechnology'), (8, b'Architecture'), (9, b'Mathematics'), (10, b'Nanotechnology'), (11, b'Chemistry'), (12, b'SOMS')])),
                ('earned_balance', models.IntegerField(default=0)),
                ('hp_balance', models.IntegerField(default=0)),
                ('post', models.IntegerField(choices=[(1, b'Ad-Hoc'), (2, b'Assistant Professor'), (3, b'Associate Professor'), (4, b'HOD'), (5, b'Professor')])),
                ('email', models.EmailField(max_length=75)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TransactionLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('earned_balance', models.IntegerField()),
                ('earned_change', models.IntegerField(default=0)),
                ('hp_balance', models.IntegerField()),
                ('hp_change', models.IntegerField(default=0)),
                ('note', models.TextField(max_length=100, null=True, blank=True)),
                ('time', models.DateTimeField(null=True)),
                ('action', models.ForeignKey(to='leave.Action', null=True)),
                ('application', models.ForeignKey(to='leave.Application', null=True)),
                ('employee', models.ForeignKey(to='leave.Employee')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_type', models.IntegerField(choices=[(0, b''), (1, b'Section Head'), (2, b'Est. Office'), (4, b'Deputy Registrar'), (5, b'Data Entry')])),
                ('dept', models.IntegerField(default=0, choices=[(0, b'Other'), (1, b'Computer Science'), (2, b'Mechanical'), (3, b'Electrical'), (4, b'Civil'), (5, b'Electronics'), (6, b'Chemical'), (7, b'Biotechnology'), (8, b'Architecture'), (9, b'Mathematics'), (10, b'Nanotechnology'), (11, b'Chemistry'), (12, b'SOMS')])),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='application',
            name='employee',
            field=models.ForeignKey(to='leave.Employee'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='application',
            name='original',
            field=models.ForeignKey(to='leave.Application', null=True),
            preserve_default=True,
        ),
    ]
