"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from openparty.apps.twitter.models import Tweet

class TweetTest(TestCase):
    def test_search(self):
        tweets = Tweet.objects.search(query='#openparty', limit=1)
        t = tweets[0]
        self.assertTrue(t.text)
    


__test__ = {}
