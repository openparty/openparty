# -*- coding: utf-8 -*-
from django.db import models

from openparty.apps.member.models import Member
from openparty.apps.core.models import Attachable


class Vote(Attachable):
    '''A Vote for Topic, Event or Comment'''
    user = models.ForeignKey(Member, related_name='vote_created',verbose_name=u"用户")
    rating = models.FloatField("评分",default=0)
    
    def __unicode__(self):
        return u'%s 投票给 %s' % (self.user, self.item)
