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

    #englishname?
    #url_path = models.SlugField(_('url path'),max_length=250, db_index=True, blank=True)
    #Currently using ID in url

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
    author = models.ForeignKey(User, related_name='topic_created', verbose_name="演讲者")
    in_event = models.ForeignKey(Event, related_name='topic_shown_in', blank=True, null=True, verbose_name="已安排在此活动中") 
    description = models.TextField("简介", max_length=200, blank=False)
    content = models.TextField("内容", blank=False)

    @property
    def is_shown(self):
        '''该话题所属活动是否正在进行或已经结束'''
        if self.in_event is not None:
            if self.in_event.is_off == True:
                return True
            elif self.in_event.is_running == True:
                return True
            else:
                return False
        else:
            return False

    @property
    def is_arranged(self):
        '''该话题是否已经加入到活动，并且活动尚未开始'''
        if self.in_event is not None:
            if self.in_event.is_upcomming == True:
                return True
            else:
                return False
        else:
            return False

    def __unicode__(self):
            return self.name

    '''#TODO Add a custom manager for most web voted & unshown topics, to add to a upcoming event'''

class Comment(Attachable):
    author = models.ForeignKey(User, related_name='comment_created',verbose_name="作者")
    content = models.TextField("内容")

    def __unicode__(self):
        return u'%s 对 %s 的评论： %s' % (self.user, self.item, self.content)

class Fav(Attachable):
    ''' A Favourite action.''' 
    user = models.ForeignKey(User, related_name='favourites',verbose_name="用户") 

    def __unicode__(self):
        return u'%s 收藏了 %s' % (self.user, self.item)

class Vote(Attachable):
    '''A Vote for Topic, Event or Comment'''
    user = models.ForeignKey(User, related_name='vote_created',verbose_name="用户")
    rating = models.FloatField("评分",default=0)
    
    def __unicode__(self):
        return u'%s 投票给 %s' % (self.user, self.item)

