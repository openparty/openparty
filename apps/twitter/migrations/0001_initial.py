# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Tweet'
        db.create_table('twitter_tweet', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tweet_id', self.gf('django.db.models.fields.BigIntegerField')(unique=True)),
            ('profile_image', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=512, blank=True)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('geo', self.gf('django.db.models.fields.CharField')(max_length=80, null=True, blank=True)),
            ('tweet_user_id', self.gf('django.db.models.fields.BigIntegerField')(blank=True)),
            ('tweet_user_name', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('craeted_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=80, null=True, blank=True)),
            ('dump', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('query', self.gf('django.db.models.fields.CharField')(max_length=127, null=True, blank=True)),
        ))
        db.send_create_signal('twitter', ['Tweet'])


    def backwards(self, orm):
        
        # Deleting model 'Tweet'
        db.delete_table('twitter_tweet')


    models = {
        'twitter.tweet': {
            'Meta': {'object_name': 'Tweet'},
            'craeted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'dump': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'geo': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'profile_image': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'query': ('django.db.models.fields.CharField', [], {'max_length': '127', 'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'tweet_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'}),
            'tweet_user_id': ('django.db.models.fields.BigIntegerField', [], {'blank': 'True'}),
            'tweet_user_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['twitter']
