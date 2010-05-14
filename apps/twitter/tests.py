"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from django.db import models
from openparty.apps.twitter.models import Tweet

class TweetTest(TestCase):
    def test_search(self):
        tweets = Tweet.objects.search(query='#openparty', limit=1)
        t = tweets[0]
        self.assertTrue(t.text)
    
    def test_sync(self):
        tweets = Tweet.objects.search(query='#openparty', limit=2)
        new = tweets[0]
        old = tweets[1]
        self.assertTrue(new.tweet_id > old.tweet_id)
        old.save()
        self.assertEquals(1, Tweet.objects.count())
        new_tweets = Tweet.objects.sync(query='#openparty', since=old.tweet_id)
        self.assertTrue(new_tweets)
        self.assertTrue(Tweet.objects.count() > 1)

__test__ = {}
