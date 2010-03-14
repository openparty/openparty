# -*- coding: utf-8 -*-
from django.db import models

from openparty.apps.member.models import Member
from openparty.apps.core.models import Attachable


class Comment(Attachable):
    author = models.ForeignKey(Member, related_name='comment_created',verbose_name=u"作者")
    content = models.TextField(u"内容")

    def __unicode__(self):
        return u'%s 对 %s 的评论： %s' % (self.user, self.item, self.content)