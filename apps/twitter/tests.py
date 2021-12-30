# -*- coding: utf-8 -*-
"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""
from unittest import skip

from apps.twitter.models import Tweet
from django.test import TestCase
from django.urls import reverse


class StatusTest(TestCase):
    def test_tweetspage(self):
        """测试tweets页面能否正常显示"""
        response = self.client.get(reverse("tweets"))
        self.failUnlessEqual(response.status_code, 200)


class TweetTest(TestCase):
    @skip("twett's authentication mechenism is changed, we need to fix it")
    def test_search(self):
        tweets = Tweet.objects.search(query="#openparty", limit=1)
        t = tweets[0]
        self.assertTrue(t.text)

    @skip("twett's authentication mechenism is changed, we need to fix it")
    def test_sync(self):
        tweets = Tweet.objects.search(query="#openparty", limit=2)
        new = tweets[0]
        old = tweets[1]
        self.assertTrue(new.tweet_id > old.tweet_id)
        old.save()
        self.assertEquals(1, Tweet.objects.count())
        new_tweets = Tweet.objects.sync(query="#openparty", since=old.tweet_id)
        self.assertTrue(new_tweets)
        self.assertTrue(Tweet.objects.count() > 1)


__test__ = {}
