# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Employee'
        db.create_table(u'leave_employee', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=10, null=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('dept', self.gf('django.db.models.fields.IntegerField')()),
            ('leave_balance', self.gf('django.db.models.fields.IntegerField')()),
            ('post', self.gf('django.db.models.fields.IntegerField')()),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
        ))
        db.send_create_signal(u'leave', ['Employee'])

        # Adding model 'UserProfile'
        db.create_table(u'leave_userprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('user_type', self.gf('django.db.models.fields.IntegerField')()),
            ('dept', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'leave', ['UserProfile'])

        # Adding model 'Application'
        db.create_table(u'leave_application', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('employee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['leave.Employee'])),
            ('leave_type', self.gf('django.db.models.fields.IntegerField')()),
            ('date_from', self.gf('django.db.models.fields.DateField')()),
            ('date_to', self.gf('django.db.models.fields.DateField')()),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('current_position', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('reason', self.gf('django.db.models.fields.TextField')(max_length=200)),
            ('attachments', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('time_generated', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('time_apporoved', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'leave', ['Application'])

        # Adding model 'CancelRequest'
        db.create_table(u'leave_cancelrequest', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['leave.Application'])),
            ('reason', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('date_from', self.gf('django.db.models.fields.DateField')()),
            ('date_to', self.gf('django.db.models.fields.DateField')()),
            ('status', self.gf('django.db.models.fields.IntegerField')()),
            ('current_position', self.gf('django.db.models.fields.IntegerField')()),
            ('time_generated', self.gf('django.db.models.fields.DateTimeField')()),
            ('time_apporoved', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'leave', ['CancelRequest'])


    def backwards(self, orm):
        # Deleting model 'Employee'
        db.delete_table(u'leave_employee')

        # Deleting model 'UserProfile'
        db.delete_table(u'leave_userprofile')

        # Deleting model 'Application'
        db.delete_table(u'leave_application')

        # Deleting model 'CancelRequest'
        db.delete_table(u'leave_cancelrequest')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'leave.application': {
            'Meta': {'object_name': 'Application'},
            'attachments': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'current_position': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'date_from': ('django.db.models.fields.DateField', [], {}),
            'date_to': ('django.db.models.fields.DateField', [], {}),
            'employee': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['leave.Employee']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'leave_type': ('django.db.models.fields.IntegerField', [], {}),
            'reason': ('django.db.models.fields.TextField', [], {'max_length': '200'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'time_apporoved': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'time_generated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'leave.cancelrequest': {
            'Meta': {'object_name': 'CancelRequest'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['leave.Application']"}),
            'current_position': ('django.db.models.fields.IntegerField', [], {}),
            'date_from': ('django.db.models.fields.DateField', [], {}),
            'date_to': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'time_apporoved': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'time_generated': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'leave.employee': {
            'Meta': {'object_name': 'Employee'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'dept': ('django.db.models.fields.IntegerField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'leave_balance': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'post': ('django.db.models.fields.IntegerField', [], {})
        },
        u'leave.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'dept': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'user_type': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['leave']