# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Application.is_credit'
        db.add_column(u'leave_application', 'is_credit',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Application.days'
        db.add_column(u'leave_application', 'days',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


        # Changing field 'Application.date_from'
        db.alter_column(u'leave_application', 'date_from', self.gf('django.db.models.fields.DateField')(null=True))

        # Changing field 'Application.date_to'
        db.alter_column(u'leave_application', 'date_to', self.gf('django.db.models.fields.DateField')(null=True))

    def backwards(self, orm):
        # Deleting field 'Application.is_credit'
        db.delete_column(u'leave_application', 'is_credit')

        # Deleting field 'Application.days'
        db.delete_column(u'leave_application', 'days')


        # User chose to not deal with backwards NULL issues for 'Application.date_from'
        raise RuntimeError("Cannot reverse this migration. 'Application.date_from' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Application.date_from'
        db.alter_column(u'leave_application', 'date_from', self.gf('django.db.models.fields.DateField')())

        # User chose to not deal with backwards NULL issues for 'Application.date_to'
        raise RuntimeError("Cannot reverse this migration. 'Application.date_to' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Application.date_to'
        db.alter_column(u'leave_application', 'date_to', self.gf('django.db.models.fields.DateField')())

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
            'attachment1': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'attachment2': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'attachment3': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'date_from': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'date_to': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'days': ('django.db.models.fields.IntegerField', [], {}),
            'employee': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['leave.Employee']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_credit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_new': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'leave_type': ('django.db.models.fields.IntegerField', [], {}),
            'new_date_from': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'new_date_to': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'original': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['leave.Application']", 'null': 'True'}),
            'reason': ('django.db.models.fields.TextField', [], {'max_length': '200'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'time_approved': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'time_generated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'time_received': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        u'leave.applicationlog': {
            'Meta': {'object_name': 'ApplicationLog'},
            'activity': ('django.db.models.fields.TextField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['leave.Application']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'leave.employee': {
            'Meta': {'object_name': 'Employee'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'unique': 'True', 'null': 'True'}),
            'dept': ('django.db.models.fields.IntegerField', [], {}),
            'earned_balance': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'hp_balance': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'post': ('django.db.models.fields.IntegerField', [], {})
        },
        u'leave.transactionlog': {
            'Meta': {'object_name': 'TransactionLog'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['leave.Application']", 'null': 'True'}),
            'earned_balance': ('django.db.models.fields.IntegerField', [], {}),
            'earned_change': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'employee': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['leave.Employee']"}),
            'hp_balance': ('django.db.models.fields.IntegerField', [], {}),
            'hp_change': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'note': ('django.db.models.fields.TextField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
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