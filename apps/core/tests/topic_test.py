# -*- coding: utf-8 -*-
from django.test import TestCase
from apps.core.models import Topic
from apps.core.tests import test_helper

class TopicTest(TestCase):
    def test_topic_summary(self):
        content = '''软件需求遇到的最大问题是什么？基本上都是沟通和交流的相关问题需求从哪里来：客户（市场）、用户 我们需要确定的是：谁是用户？当前业务流程情况？业务目标是什么？ 项目需求确定中遇到的最大问题是什么？需求文档驱动的过程不堪重负 查看更多'''
        t = Topic(content=content)
        self.assertEquals(u'软件需求遇到的最大问题是什么？...', t.summary)
    
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

    #TODO 需要给submit_topic添加一个测试
