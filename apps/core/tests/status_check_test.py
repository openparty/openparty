# -*- coding: utf-8 -*-

from django.test import TestCase
from django.core.urlresolvers import reverse
from apps.member.models import Member
from apps.core.models import Event, Topic
from django.contrib.auth.models import User
from datetime import datetime

class StatusCheckTest(TestCase):
    def setUp(self):
        new_user = User.objects.create(username="tester", password="tester")
        new_user.save()
        self.client.login(username="tester", passsword="tester")
        new_member = Member.objects.create(user=new_user, nickname="tester")
        new_member.save()
        new_event = Event.objects.create(name="test event 01", description="xxx", content="xxx", begin_time = datetime.now(), end_time = datetime.now(), last_modified_by=new_member)
        new_event.save()
        new_topic = Topic.objects.create(name="test topic 01", description="xxx", content="xxx", author=new_member, last_modified_by=new_member)
        new_topic.save()

    def test_statuscheck_indexpage(self):
        response = self.client.get("/")
        #Check the response status
        self.failUnlessEqual(response.status_code, 200)
        #check template usage

    def test_statuscheck_eventlistpage(self):
        response = self.client.get("/event")
        self.failUnlessEqual(response.status_code, 200)

    def test_statuscheck_topiclist_page(self):
        response = self.client.get("/topics")
        self.failUnlessEqual(response.status_code, 200)

    def test_statuscheck_eventdetail_page(self):
        response = self.client.get("/event/1")
        self.failUnlessEqual(response.status_code, 200)
        response = self.client.get("/event/19999")
        self.failUnlessEqual(response.status_code, 404)

    def test_statuscheck_topicdetail_page(self):
        response = self.client.get("/topic/1")
        self.failUnlessEqual(response.status_code, 200)
        response = self.client.get("/topic/19999")
        self.failUnlessEqual(response.status_code, 404)

    def statuscheck_topicsubmit_page(self):
        response = self.client.get(reverse('submit_new_topic'))
        self.failUnlessEqual(response.status_code, 200)

    def statuscheck_eventjoin_page(self):
        response = self.client.get('/event/join')
        self.failUnlessEqual(response.status_code, 200)

    def test_statuscheck_topicvotedetail_page(self):
        response = self.client.get("/topic/1/votes")
        self.failUnlessEqual(response.status_code, 200)
        response = self.client.get("/topic/19999/votes")
        self.failUnlessEqual(response.status_code, 404)


