# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from abstract import Base, Attachable


import datetime

class Event(Base):
    datetime_begin = models.DateTimeField("开始时间", auto_now_add=False, auto_now=False, blank=False, null=False)
    datetime_end = models.DateTimeField("结束时间", auto_now_add=False, auto_now=False, blank=False, null=False)
    description = models.TextField("简介", max_length=200, blank=False)
    content = models.TextField("介绍", blank=False)

    @property
    def is_running(self):
        return datetime.datetime.now() > self.datetime_begin and datetime.datetime.now() < self.datetime_end

    @property
    def is_off(self):
        return datetime.datetime.now() > self.datetime_end

    @property
    def is_upcoming(self):
        return datetime.datetime.now() < self.datetime_begin

    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.datetime_begin) 


class Topic(Base):
    author = models.ForeignKey(User, related_name='topic_created')
    shown_in_event = models.ForeignKey(Event, related_name='topic_shown_in', blank=True, null=True, verbose_name="已在此活动中宣讲") 
    arranged_in_event = models.ForeignKey(Event, related_name='topic_arranged_in', blank=True, null=True, verbose_name="已安排在此活动中")
    #TODO 将这两个合为一个
    description = models.TextField("简介", max_length=200, blank=False)
    content = models.TextField("内容", blank=False)

    @property
    def is_shown(self):
        return self.shown_in_event != None

    @property
    def is_arranged(self):
        '''if a topic is (attached or related) to an event'''
        return self.arranged_in_event != None

    def __unicode__(self):
            return self.name

    '''#TODO Add a custom manager for most web voted & unshown topics, to add to a upcoming event'''

class Comment(Attachable):
    author = models.ForeignKey(User, related_name='comment_created',verbose_name="作者")
    content = models.TextField("内容")

class Fav(Attachable):
    ''' A Favourite action.''' 
    user = models.ForeignKey(User, related_name='favourites',verbose_name="用户") 

class Vote(Attachable):
    '''A Vote for Topic, Event or Comment'''
    user = models.ForeignKey(User, related_name='vote_created',verbose_name="用户")
    rating = models.FloatField("评分",default=0)
    
    def __unicode__(self):
        return u'%s 投票给 %s' % (self.user, self.item)

