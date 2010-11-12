# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models, connection, transaction


class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Tweet.race'
        db.add_column('twitter_tweet', 'race', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True), keep_default=False)

        # Adding field 'Tweet.uri'
        db.add_column('twitter_tweet', 'uri', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True), keep_default=False)

        # Changing field 'Tweet.text'
        db.alter_column('twitter_tweet', 'text', self.gf('django.db.models.fields.TextField')(max_length=512, blank=True))
        db.execute("update twitter_tweet set race = 'twitter' where race is null")

    def backwards(self, orm):
        
        # Deleting field 'Tweet.race'
        db.delete_column('twitter_tweet', 'race')

        # Deleting field 'Tweet.uri'
        db.delete_column('twitter_tweet', 'uri')

        # Changing field 'Tweet.text'
        db.alter_column('twitter_tweet', 'text', self.gf('django.db.models.fields.CharField')(max_length=512, blank=True))


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
            'race': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'max_length': '512', 'blank': 'True'}),
            'tweet_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'}),
            'tweet_user_id': ('django.db.models.fields.BigIntegerField', [], {'blank': 'True'}),
            'tweet_user_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'uri': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['twitter']
