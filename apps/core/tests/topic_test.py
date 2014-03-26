# -*- coding: utf-8 -*-
from django.test import TestCase
from apps.core.models import Topic
from apps.core.tests import test_helper
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from apps.member.models import Member
import apps.member.test_helper as helper

class TopicTest(TestCase):
    def test_topic_summary(self):
        content = '''软件需求遇到的最大问题是什么？基本上都是沟通和交流的相关问题需求从哪里来：客户（市场）、用户 我们需要确定的是：谁是用户？当前业务流程情况？业务目标是什么？ 项目需求确定中遇到的最大问题是什么？需求文档驱动的过程不堪重负 查看更多'''
        t = Topic(content=content)
        self.assertEquals(u'软件需求遇到的最大问题是什么？基本上都是沟通和交流的相关问题需求从哪里来：客户（市场）、用户 我们需要确定的是：谁是用户...', t.summary)
    
    def test_render_topic_content_restructuredtext(self):
        '''You have to install docutils for pass this test.'''
        content = '标题\n- point 1\n- point 2'
        t = Topic(content=content)
        self.assertEquals(u'<p>标题\n- point 1\n- point 2</p>\n', t.rendered_content)
    
    def test_render_topic_content_html(self):
        html = '<h2>标题</h2><p>内容</p>'
        t = Topic(html=html, content_type='html')
        self.assertEquals(html, t.rendered_content)
    
    def test_topic_poll_status_when_it_is_not_in_event(self):
        event = test_helper.create_passed_event()
        topic = Topic(name='test', content='test', description='', author=event.last_modified_by, accepted=True)
        topic.last_modified_by=event.last_modified_by
        topic.save()
        self.assertEquals(u'该话题尚未加入任何活动，无法开始投票', topic.poll_status)
        # it's not related to accepted
        topic.accepted = False
        topic.save()
        self.assertEquals(u'该话题尚未加入任何活动，无法开始投票', topic.poll_status)
    
    def test_topic_poll_status_when_it_is_not_accepted_by_admin(self):
        event = test_helper.create_passed_event()
        topic = Topic(name='test', content='test', description='', in_event=event, author=event.last_modified_by, accepted=False)
        topic.last_modified_by=event.last_modified_by
        topic.save()
        self.assertEquals(u'活动等待管理员审核中，审核完毕后即可开始投票', topic.poll_status)
    
    def test_topic_poll_status(self):
        event = test_helper.create_upcoming_event()
        topic = Topic(name='test', content='test', description='', in_event=event, author=event.last_modified_by, accepted=True)
        topic.last_modified_by=event.last_modified_by
        topic.save()
        self.assertEquals(u'网络投票进行中', topic.poll_status)

    def test_topic_poll_status_when_event_is_passed(self):
        event = test_helper.create_passed_event()
        topic = Topic(name='test', content='test', description='', in_event=event, author=event.last_modified_by, accepted=True)
        topic.last_modified_by=event.last_modified_by
        topic.save()
        self.assertEquals(u'本话题所属活动已经结束', topic.poll_status)

    def test_topic_model_refactor_last_modified_by_reverse_search(self):
        '''针对core中models合并后FK外键反向查找中%(class)s是否正常工作的测试(可删除)'''
        event = test_helper.create_upcoming_event()
        topic = Topic(name='test', content='test', description='', in_event=event, author=event.last_modified_by, accepted=True)
        topic.last_modified_by=event.last_modified_by
        topic.save()
        topic_should_be = event.last_modified_by.topic_last_modified.all()[0]
        self.failUnlessEqual(topic, topic_should_be)

    def test_submit_topic(self):
        '''用户登录后可以成功提交话题'''
        new_user = User.objects.create_user("tin", "tin@tin.com", "123")
        self.client.login(username='tin', password='123')
        Member.objects.create(user = new_user, nickname="Tin")
        event = test_helper.create_upcoming_event()
        response = self.client.post(reverse("submit_new_topic"), {'name':'Test Topic Submitted','title':'','description':'Test Topic Description','content':'content','in_event':event.id, 'captcha':''})
        check_topic = len(Topic.objects.filter(name="Test Topic Submitted"))
        self.assertEquals(1, check_topic)

    def test_captcha_on_submit(self):
        '''填写了不可见字段的话题被视为spam不可提交'''
        new_user = User.objects.create_user("tin", "tin@tin.com", "123")
        self.client.login(username='tin', password='123')
        Member.objects.create(user = new_user, nickname="Tin")
        event = test_helper.create_upcoming_event()
        response = self.client.post(reverse("submit_new_topic"), {"title":"iamaspamer",'name':'Test Topic Submitted','description':'Test Topic Description','content':'content','in_event':event.id, 'captcha':'should be empty if human'})
        self.assertEquals(response.status_code, 403)

    def test_edit_topic(self):
        '''用户登录后可以修改自己提交的话题'''

        new_user = User.objects.create_user("test", "test@test.com", "123")
        member_new_user = Member.objects.create(user = new_user, nickname="Test")
        self.client.login(username='test', password='123')

        event = test_helper.create_upcoming_event()
        
        test_user_topic = Topic.objects.create(author = member_new_user, in_event = event, \
                                               name = "Test", description = "test", content = "test")

        response = self.client.get(reverse("edit_topic",  kwargs = {"id": test_user_topic.id }))
        self.failUnlessEqual(response.status_code, 200)

        #如果用户不是此话题的作者，则无法编辑此话题

        non_relevant_user = User.objects.create_user("another_user", "another@test.com", "123")
        member_non_relevant_user = Member.objects.create(user = non_relevant_user, nickname="Another")

        test_non_user_topic = Topic.objects.create(author = member_non_relevant_user, in_event = event, \
                                                   name = "Another Topic", description = "test", content = "test")
        response = self.client.get(reverse("edit_topic", kwargs = {"id": test_non_user_topic.id }))
        self.failUnlessEqual(response.status_code, 302)


