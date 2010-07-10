# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models
from apps.member.models import Member

class EventManager(models.Manager):
    def next_event(self):
        '''定义next_event为获取当前未结束的活动或下次活动，减少逻辑复杂度'''
        latest_nonclosed_events = super(EventManager, self).get_query_set().filter(end_time__gte=datetime.now()).order_by("begin_time")
        if latest_nonclosed_events.count() >= 1:
            next_event = latest_nonclosed_events[0]
            next_event.css_class = 'hot'
            return next_event 
        else:
            return NullEvent()

    def upcoming_events(self):
        return super(EventManager, self).get_query_set().filter(begin_time__gte=datetime.now())

    def past_events(self):
        return super(EventManager, self).get_query_set().filter(end_time__lte=datetime.now())

class NullEventException(Exception):
    pass

class NullEvent(object):
    id = 0
    '''空的项目，保持接口的一致'''
    begin_time  = u'未定'
    end_time    = u'未定'
    description = u'本次活动正在计划中'
    content     = u'本次活动正在计划中'
    address     = u'东直门国华投资大厦11层'
    poster      = '/media/upload/null-event-1.jpg'
    participants = set()
    
    css_class   = 'inactive'
    
    def save():
        raise NullEventException()
    
    is_running  = False
    is_off      = False
    is_upcoming = True

class Event(models.Model):
    begin_time  = models.DateTimeField(u"开始时间", auto_now_add=False, auto_now=False, blank=False, null=False)
    end_time    = models.DateTimeField(u"结束时间", auto_now_add=False, auto_now=False, blank=False, null=False)
    description = models.TextField(u"简介", max_length=200, blank=False)
    content     = models.TextField(u"介绍", blank=False)
    address     = models.TextField(u"活动地点", blank=False)
    poster      = models.CharField(u"招贴画", default='/media/upload/null-event-1.jpg', blank=True, max_length=255)
    participants = models.ManyToManyField(Member, related_name='joined_%(class)s')
    appearances = models.ManyToManyField(Member, related_name='arrived_%(class)s')
    
    css_class   = ''

    name = models.CharField("名称", max_length=255, blank=False)
    created = models.DateTimeField(auto_now_add=True, auto_now=True, blank=True, null=True)
    last_modified = models.DateTimeField(auto_now_add=True, auto_now=True, blank=True, null=True)
    last_modified_by = models.ForeignKey(Member, related_name='%(class)s_last_modified')
    #aggrgated
    total_votes = models.PositiveIntegerField(default=0)
    total_favourites = models.PositiveIntegerField(default=0, editable=False)


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
    
    class Meta:
        app_label = 'core'

    objects = EventManager()
