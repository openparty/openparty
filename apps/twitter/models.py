# -*- coding: utf-8 -*-
import json
import tweepy

import time
from django.db import models

class TweetManager(models.Manager):
    def search(self, query='#openparty', limit=5, since=None, page=1):
        tweets = tweepy.api.search(q=query, rpp=limit, since_id=since, page=page)
        return [self.model(tweet=tweet) for tweet in tweets]
    
    def sync(self, query='#openparty', since=None):
        if since:
            max_tweet_id = since # for test only
        else:
            max_tweet_id = self.filter(query=query).aggregate(models.Max('tweet_id'))['tweet_id__max']
        print 'Syncing new tweets of %s (newer than %s)' % (query, max_tweet_id)
        new_tweets = self.search(query=query, limit=100, since=max_tweet_id, page=1)
        if len(new_tweets):
            for tweet in new_tweets:
                tweet.query = query
                tweet.save()
            return len(new_tweets)
        else:
            return 0
    
    def sync_all(self, query='#openparty'):
        page = 1
        count = 0
        print 'Syncing all of %s' % query
        while True:
            tweets = tweepy.api.search(q=query, rpp=50, page=page)
            page += 1
            if len(tweets) == 0:
                break
            for tweet in tweets:
                t = self.model(tweet=tweet)
                t.query = query
                t.save()
                count += 1
            print 'synced %s tweets' % count
            time.sleep(5)
        return count

# Create your models here.
class Tweet(models.Model):
    """(A model represent the tweets of twitter.com)"""
    tweet_id = models.BigIntegerField(blank=False, null=False, unique=True)
    profile_image = models.CharField(blank=True, null=True, max_length=255)
    text = models.CharField(blank=True, null=False, max_length=512)
    language = models.CharField(blank=True, null=True, max_length=16)
    geo = models.CharField(blank=True, null=True, max_length=80)
    tweet_user_id = models.BigIntegerField(blank=True, null=False)
    tweet_user_name = models.CharField(blank=True, null=True, max_length=128)
    craeted_at = models.DateField(blank=False, null=True)
    source = models.CharField(blank=True, null=True, max_length=80)
    dump = models.TextField(blank=True, null=False)
    query = models.CharField(blank=True, null=True, max_length=127)
    
    objects = TweetManager()
    
    def __init__(self, tweet, *args, **kwargs):
        super(Tweet, self).__init__(*args, **kwargs)
        if isinstance(tweet, tweepy.models.SearchResult):
            self.tweet_id = tweet.id
            self.profile_image = tweet.profile_image_url
            self.text = tweet.text
            self.language = tweet.iso_language_code
            self.geo = tweet.geo
            self.tweet_user_id = tweet.from_user_id
            self.tweet_user_name = tweet.from_user
            self.created_at = tweet.created_at
            self.source = tweet.source
            d = tweet.__dict__.copy()
            d.pop('created_at')
            self.dump = json.dumps(d)

    class Meta:
        ordering = []
        verbose_name, verbose_name_plural = "Tweet", "s"

    def __unicode__(self):
        return u"Tweet"

    @models.permalink
    def get_absolute_url(self):
        return ('Tweet', [self.id])