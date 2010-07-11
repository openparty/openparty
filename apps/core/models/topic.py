# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models
from django.conf import settings
from django.core import mail
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.template.loader import render_to_string
from django.contrib.markup.templatetags.markup import restructuredtext
from django.core.urlresolvers import reverse

from apps.member.models import Member
from apps.core.models import Event
from apps.core.models.vote import Vote

class Topic(models.Model):

    author = models.ForeignKey(Member, related_name='topic_created', verbose_name=u"演讲者")
    in_event = models.ForeignKey(Event, related_name='topic_shown_in', blank=True, null=True, verbose_name=u"已安排在此活动中") 
    description = models.TextField(u"简介", max_length=200, blank=False)
    content = models.TextField(u"内容", blank=False)
    html = models.TextField(u'HTML', blank=True, null=True)
    content_type = models.CharField(blank=False, default='restructuredtext', max_length=30)
    accepted = models.BooleanField(default=False)  #该话题是否已经被管理员接受,True才能在活动正式的公布页面显示, 同时in_event才能显示
    
    name = models.CharField("名称", max_length=255, blank=False)
    created = models.DateTimeField(auto_now_add=True, auto_now=True, blank=True, null=True)
    last_modified = models.DateTimeField(auto_now_add=True, auto_now=True, blank=True, null=True)
    last_modified_by = models.ForeignKey(Member, related_name='%(class)s_last_modified')
    #aggrgated
    total_votes = models.PositiveIntegerField(default=0)
    total_favourites = models.PositiveIntegerField(default=0, editable=False)

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
            '''暂时取消restructuredtext的处理'''
            #return restructuredtext(self.content)
            return self.content
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
    
    def style_seed(self, range=4):
        '''用来显示一些随机的样式'''
        return self.id % range

    def get_absolute_url(self):
        return reverse('topic', args = [self.id])

    def send_notification_mail(self, type):
        '''在话题提交及更新时发送提醒邮件'''
       
        type_dict = {'created':u'建立',
                     'updated':u'更新',
                    }
        subject = u"[Open Party] 话题%(type)s：%(name)s" % {'type':type_dict[type.lower()], 'name':self.name}

        ctx = { 'topic': self,
                'action': type_dict[type.lower()],
                'modification_date': str(datetime.now()),
                'site': settings.SITE_URL }

        message = render_to_string('core/topic_notification_email.txt', ctx)

        admin_user_set = User.objects.filter(is_staff = True) #给具有管理权限的用户发信
        #没有用mail_admins(),更灵活一些
        mail_queue = []
        for each_admin in admin_user_set:
            email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, 
            [each_admin.email], '',
            headers = {'Reply-To': each_admin.email})
            email.content_subtype = "plain"
            mail_queue.append(email)

        #使用单次SMTP连接批量发送邮件
        connection = mail.get_connection()   # Use default e-mail connection
        connection.send_messages(mail_queue)

        return True

    def __unicode__(self):
            return self.name

    votes = generic.GenericRelation('Vote')

    #TODO Add a custom manager for most web voted & unshown topics, to add to a upcoming event

    def save(self, *args, **kwargs):
        self.total_votes = self.votes.count()
        super(Topic, self).save(*args, **kwargs)
    
    class Meta:
        app_label = 'core'
