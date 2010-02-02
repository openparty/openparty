# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


import datetime

class Base(models.Model):
    name = models.CharField(max_length=255, blank=False)
    total_favourites = PositiveIntegerFiled(default=0, editable=False)

    created = models.DateTimeField(auto_now_add=True, auto_now=True, blank=True, null=True)
    deleted = models.DateTimeField(auto_now_add=True, auto_now=True, blank=True, null=True)

    last_modified = models.DateTimeField(auto_now_add=True, auto_now=True, blank=True, null=True)
    #last_modifier = models.ForeignKey(Member, related_name='', limit_choices_to=, to_field='')

    vote = models.IntegerField()

    class Meta:
        abstract = True

class Attachable(models.Model):
    conntent_type = models.ForeignKey(ContentType, limit_choices_to = {'model__in': ('topic', 'event', 'comment')})
    object_id = models.PositiveIntegerField(_('object id'),)
    item = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        abstract = True


class Event(Base):
    datetime_begin = models.DateTimeField(auto_now_add=False, auto_now=False, blank=False, null=False)
    datetime_end = models.DateTimeField(auto_now_add=False, auto_now=False, blank=False, null=False)
    content = models.TextField(blank=False)

    #denorm
    count_user_attending = models.PositiveIntegerField()
    count_user_following = models.PositiveIntegerField()

    @property
    def is_running(self):
        return datetime.datetime.now() > self.datetime_begin and datetime.datetime.now() < self.datetime_end

    @property
    def is_off(self):
        return datetime.datetime.now() > self.datetime_end

    @property
    def is_upcoming(self):
        return datetime.datetime.now() < self.datetime_begin

    @property
    def is_theupcoming(self):
        '''Check if this event is the latest upcoming one.'''
        return datetime.datetime.now() < self.datetime_begin

    def __init__(self, arg):
        super(ClassName, self).__init__()
        self.arg = arg

    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.datetime_begin) 


class Topic(Base):

    author = models.ForeignKey(OtherModel, related_name='', limit_choices_to=, to_field='')
    shown_in_event = models.ForeignKey(OtherModel, related_name='', limit_choices_to=, to_field='')
    vote_web = models.IntegerField()
    vote_live = models.IntegerField()
    content = models.TextField(blank=True)

    @property
    def is_shown(self):
        return self.shown_in_event != None

    @property
    def is_arranged(self):
        return 'if a topic is (attached or related) to an event'

class Comment(Attachable):
    
    content = models.TextField(_('content'),)
    author = models.ForeignKey(User, related_name='',verbose_name=_('author'))

class Fav(Attachable):
    ''' A Favourite action.''' 
    user = models.ForeignKey(User, related_name='favourites',verbose_name=_('user')) 
    created = models.DateTimeField(_('created'),auto_now_add=True) 

    # denorm 
    item_raw = models.TextField(_('item raw'),blank=True) 
    user_raw = models.TextField(_('user raw'),blank=True) 
 

