#!/usr/bin/env python
# encoding: utf-8
from datetime import datetime, timedelta
from django.test import TestCase
from apps.core.models import Event
from apps.member import test_helper as member_test_helper

class EventTests(TestCase):

    def setUp(self):
        self.yesterday = datetime.now() - timedelta(days=1)
        self.the_day_before_yesterday = datetime.now() - timedelta(days=2)
        self.tomorrow = datetime.now() + timedelta(days=1)
        self.member = member_test_helper.create_user()

    def tearDown(self):
        pass
    
    def test_passed_event_is_not_upcoming_event(self):
        event = Event(begin_time=self.the_day_before_yesterday, end_time=self.yesterday, name='test', content='test')
        event.last_modified_by = self.member
        event.save()
        self.assertFalse(event.is_upcoming)
    
    def test_new_event_is_upcoming_event(self):
        event = Event(begin_time=self.tomorrow, end_time=self.tomorrow, name='test', content='test')
        event.last_modified_by = self.member
        event.save()
        self.assertTrue(event.is_upcoming)
    
    def test_event_is_off(self):
        event = Event(begin_time=self.tomorrow, end_time=self.tomorrow, name='test', content='test')
        event.last_modified_by = self.member
        event.save()
        self.assertFalse(event.is_off)
        event.end_time = self.yesterday
        event.save()
        self.assertTrue(event.is_off)
    
    def test_event_is_running(self):
        event = Event(begin_time=self.tomorrow, end_time=self.tomorrow, name='test', content='test')
        event.last_modified_by = self.member
        event.save()
        self.assertFalse(event.is_running)
        
        event.begin_time=self.yesterday
        event.end_time=self.yesterday
        event.save()
        self.assertFalse(event.is_running)
        
        event.begin_time=self.yesterday
        event.end_time= self.tomorrow
        event.save()
        self.assertTrue(event.is_running)

    def test_event_get_latest_nonclosed_event(self):
        '''获取最近一个尚未关闭的活动,用于活动现场签到'''
        event = Event(begin_time=self.the_day_before_yesterday, end_time=self.tomorrow, name='test', content='test')
        event.last_modified_by = self.member
        event.save()
        self.failUnlessEqual(Event.objects.latest_nonclosed_event(), event)

        event.end_time=self.yesterday
        event.save()
        #NullEvent的id为0
        self.assertEquals(Event.objects.latest_nonclosed_event().id, 0)

    def test_event_manager_upcoming_past_events(self):
        '''测试Manager里面的upcoming_events'''
        event = Event(begin_time=self.tomorrow, end_time=self.tomorrow, name='upcoming event', content='test')
        event.last_modified_by = self.member
        event.save()
        event_past = Event(begin_time=self.the_day_before_yesterday, end_time=self.yesterday, name='past event', content='test')
        event_past.last_modified_by = self.member
        event_past.save()

        self.failUnlessEqual(Event.objects.upcoming_events()[0], event)
        self.failUnlessEqual(Event.objects.past_events()[0], event_past)

