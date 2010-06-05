# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.markup.templatetags.markup import restructuredtext

from apps.member.models import Member
from apps.core.models import Base, Event


class Topic(Base):
    author = models.ForeignKey(Member, related_name='topic_created', verbose_name=u"演讲者")
    in_event = models.ForeignKey(Event, related_name='topic_shown_in', blank=True, null=True, verbose_name=u"已安排在此活动中") 
    description = models.TextField(u"简介", max_length=200, blank=False)
    content = models.TextField(u"内容", blank=False)
    html = models.TextField(u'HTML', blank=True, null=True)
    content_type = models.CharField(blank=False, default='restructuredtext', max_length=30)
    accepted = models.BooleanField(default=False)  #该话题是否已经被管理员接受,True才能在活动正式的公布页面显示, 同时in_event才能显示
    
    def set_author(self, user):
        author = Member.objects.get(user = user)
        self.last_modified_by = author # last_modified_by 总是author？
        self.author = author
        return self
    
    @property
    def poll_status(self):
        if self.in_event:
            if self.accepted:
                if self.in_event.is_upcoming:
                    return u'网络投票进行中'
                elif self.in_event.is_off:
                    return u'本话题所属活动已经结束'
            else:
                return u'活动等待管理员审核中，审核完毕后即可开始投票'
        else:
            return u'该话题尚未加入任何活动，无法开始投票'

        return u'我们也不知道怎么了'
    
    @property
    def rendered_content(self):
        if self.content_type == 'restructuredtext':
            return restructuredtext(self.content)
        elif self.content_type == 'html':
            return self.html
        else:
            return restructuredtext(self.content)

    @property
    def is_shown(self):
        '''该话题所属活动是否正在进行或已经结束'''
        return self.in_event and (self.in_event.is_off or self.in_event.is_running)

    @property
    def is_arranged(self):
        '''该话题是否已经加入到活动，并且活动尚未开始'''
        return self.in_event and (self.in_event.is_upcoming == True)
    
    @property
    def summary(self):
        try:
            content = self.content.decode('utf-8')
        except UnicodeEncodeError:
            content = self.content
        
        if len(content) > 15:
            return '%s...' % content[:15]
        else:
            return content

    def __unicode__(self):
            return self.name

    votes = generic.GenericRelation('Vote')

    #TODO Add a custom manager for most web voted & unshown topics, to add to a upcoming event

    def save(self, *args, **kwargs):
        self.total_votes = self.votes.count()
        super(Topic, self).save(*args, **kwargs)
