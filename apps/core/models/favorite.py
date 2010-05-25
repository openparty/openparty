# -*- coding: utf-8 -*-
from django.db import models

from apps.member.models import Member
from apps.core.models import Attachable

class Favorite(Attachable):
    ''' A Favourite action.''' 
    user = models.ForeignKey(Member, related_name='favourites',verbose_name=u"用户")

    def __unicode__(self):
        return u'%s 收藏了 %s' % (self.user, self.item)