# -*- coding: utf-8 -*-
from django.test import TestCase
from apps.core.models import Topic
from apps.core.tests import test_helper
from django.urls import reverse
from django.contrib.auth.models import User
from apps.member.models import Member
import apps.member.test_helper as helper


class FeedTest(TestCase):

    def test_topics_feed(self):
        '''测试话题的Feed能否正常输出'''

        response = self.client.post(reverse("feed_topics"))
        self.failUnlessEqual(response.status_code, 200)

    def test_events_feed(self):
        '''测试活动的Feed能否正常输出'''

        response = self.client.post(reverse("feed_events"))
        self.failUnlessEqual(response.status_code, 200)

    def test_posts_feed(self):
        '''测试新闻的Feed能否正常输出'''

        response = self.client.post(reverse("feed_posts"))
        self.failUnlessEqual(response.status_code, 200)
