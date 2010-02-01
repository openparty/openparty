# -*- coding: utf-8 -*-

from django.db import models

import datetime

class Base(models.Model):
    total_favourites = PositiveIntegerFiled(default=0, editable=False)

    created = models.DateTimeField(auto_now_add=True, auto_now=True, blank=True, null=True)
    deleted = models.DateTimeField(auto_now_add=True, auto_now=True, blank=True, null=True)

    last_modified = models.DateTimeField(auto_now_add=True, auto_now=True, blank=True, null=True)
    #last_modifier = models.ForeignKey(Member, related_name='', limit_choices_to=, to_field='')

    class Meta:
        abstract = True

class Event(Base):

    name = models.CharField(max_length=255, blank=False)
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

    def __init__(self, arg):
        super(ClassName, self).__init__()
        self.arg = arg

    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.datetime_begin) 


class Topic(Base):
    
    pass
