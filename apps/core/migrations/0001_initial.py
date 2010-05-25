# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Event'
        db.create_table('core_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, null=True, blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, null=True, blank=True)),
            ('last_modified_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='event_last_modified', to=orm['member.Member'])),
            ('total_votes', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('total_favourites', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('begin_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=200)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('address', self.gf('django.db.models.fields.TextField')()),
            ('poster', self.gf('django.db.models.fields.CharField')(default='/media/upload/null-event-1.jpg', max_length=255, blank=True)),
        ))
        db.send_create_signal('core', ['Event'])

        # Adding M2M table for field participants on 'Event'
        db.create_table('core_event_participants', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm['core.event'], null=False)),
            ('member', models.ForeignKey(orm['member.member'], null=False))
        ))
        db.create_unique('core_event_participants', ['event_id', 'member_id'])

        # Adding model 'Topic'
        db.create_table('core_topic', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, null=True, blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, null=True, blank=True)),
            ('last_modified_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='topic_last_modified', to=orm['member.Member'])),
            ('total_votes', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('total_favourites', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='topic_created', to=orm['member.Member'])),
            ('in_event', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='topic_shown_in', null=True, to=orm['core.Event'])),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=200)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('accepted', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
        ))
        db.send_create_signal('core', ['Topic'])

        # Adding model 'Vote'
        db.create_table('core_vote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('item_raw', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('user_raw', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='vote_created', to=orm['member.Member'])),
            ('rating', self.gf('django.db.models.fields.FloatField')(default=0)),
        ))
        db.send_create_signal('core', ['Vote'])

        # Adding model 'Favorite'
        db.create_table('core_favorite', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('item_raw', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('user_raw', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='favourites', to=orm['member.Member'])),
        ))
        db.send_create_signal('core', ['Favorite'])


    def backwards(self, orm):
        
        # Deleting model 'Event'
        db.delete_table('core_event')

        # Removing M2M table for field participants on 'Event'
        db.delete_table('core_event_participants')

        # Deleting model 'Topic'
        db.delete_table('core_topic')

        # Deleting model 'Vote'
        db.delete_table('core_vote')

        # Deleting model 'Favorite'
        db.delete_table('core_favorite')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.event': {
            'Meta': {'object_name': 'Event'},
            'address': ('django.db.models.fields.TextField', [], {}),
            'begin_time': ('django.db.models.fields.DateTimeField', [], {}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '200'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'last_modified_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'event_last_modified'", 'to': "orm['member.Member']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'participants': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['member.Member']", 'symmetrical': 'False'}),
            'poster': ('django.db.models.fields.CharField', [], {'default': "'/media/upload/null-event-1.jpg'", 'max_length': '255', 'blank': 'True'}),
            'total_favourites': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'total_votes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'core.favorite': {
            'Meta': {'object_name': 'Favorite'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_raw': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'favourites'", 'to': "orm['member.Member']"}),
            'user_raw': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'core.topic': {
            'Meta': {'object_name': 'Topic'},
            'accepted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'topic_created'", 'to': "orm['member.Member']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_event': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'topic_shown_in'", 'null': 'True', 'to': "orm['core.Event']"}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'last_modified_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'topic_last_modified'", 'to': "orm['member.Member']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'total_favourites': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'total_votes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'core.vote': {
            'Meta': {'object_name': 'Vote'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_raw': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'rating': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'vote_created'", 'to': "orm['member.Member']"}),
            'user_raw': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'member.member': {
            'Meta': {'object_name': 'Member'},
            'activation_key': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'properties': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['core']
