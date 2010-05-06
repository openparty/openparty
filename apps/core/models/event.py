# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models
from openparty.apps.member.models import Member
from openparty.apps.core.models import Base


class EventManager(models.Manager):
    def next_event(self):
        upcoming_events = super(EventManager, self).get_query_set().filter(begin_time__gte=datetime.now())
        if upcoming_events.count() >= 1:
            return upcoming_events.order_by("-begin_time")[0]
        else:
            return NullEvent()

class UpcomingManager(models.Manager):
    def get_query_set(self):
        return super(UpcomingManager, self).get_query_set().filter(begin_time__gte=datetime.now())

class PastManager(models.Manager):
    def get_query_set(self):
        return super(PastManager, self).get_query_set().filter(end_time__lte=datetime.now())

class NullEvent(object):
    '''空的项目，保持接口的一致'''
    begin_time  = u'未定'
    end_time    = u'未定'
    description = u'本次活动正在计划中'
    content     = u'本次活动正在计划中'
    address     = u'东直门国华投资大厦11层'
    poster      = '/media/upload/null-event-1.jpg'
    
    is_running  = False
    is_off      = False
    is_upcoming = True

class Event(Base):
    begin_time  = models.DateTimeField(u"开始时间", auto_now_add=False, auto_now=False, blank=False, null=False)
    end_time    = models.DateTimeField(u"结束时间", auto_now_add=False, auto_now=False, blank=False, null=False)
    description = models.TextField(u"简介", max_length=200, blank=False)
    content     = models.TextField(u"介绍", blank=False)
    address     = models.TextField(u"活动地点", blank=False)
    poster      = models.CharField(u"招贴画", default='/media/upload/null-event-1.jpg', blank=True, max_length=255)

    #englishname?
    #url_path = models.SlugField(_('url path'),max_length=250, db_index=True, blank=True)
    #Currently using ID in url

    @property
    def is_running(self):
        return datetime.now() > self.begin_time and datetime.now() < self.end_time

    @property
    def is_off(self):
        return datetime.now() > self.end_time

    @property
    def is_upcoming(self):
        return datetime.now() < self.begin_time

    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.begin_time)
    
    objects = EventManager()
    upcoming = UpcomingManager()
    past = PastManager()
