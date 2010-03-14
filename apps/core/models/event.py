# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models
from openparty.apps.member.models import Member
from openparty.apps.core.models import Base


class Event(Base):
    datetime_begin = models.DateTimeField(u"开始时间", auto_now_add=False, auto_now=False, blank=False, null=False)
    datetime_end = models.DateTimeField(u"结束时间", auto_now_add=False, auto_now=False, blank=False, null=False)
    description = models.TextField(u"简介", max_length=200, blank=False)
    content = models.TextField(u"介绍", blank=False)

    #englishname?
    #url_path = models.SlugField(_('url path'),max_length=250, db_index=True, blank=True)
    #Currently using ID in url

    @property
    def is_running(self):
        return datetime.now() > self.datetime_begin and datetime.datetime.now() < self.datetime_end

    @property
    def is_off(self):
        return datetime.now() > self.datetime_end

    @property
    def is_upcoming(self):
        return datetime.now() < self.datetime_begin

    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.datetime_begin)
