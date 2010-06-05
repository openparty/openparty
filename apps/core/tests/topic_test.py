# -*- coding: utf-8 -*-
from django.test import TestCase
from apps.core.models import Topic

class TopicTest(TestCase):
    def test_topic_summary(self):
        content = '''软件需求遇到的最大问题是什么？基本上都是沟通和交流的相关问题需求从哪里来：客户（市场）、用户 我们需要确定的是：谁是用户？当前业务流程情况？业务目标是什么？ 项目需求确定中遇到的最大问题是什么？需求文档驱动的过程不堪重负 查看更多'''
        t = Topic(content=content)
        self.assertEquals(u'软件需求遇到的最大问题是什么？...', t.summary)
    
    def test_render_topic_content_restructuredtext(self):
        content = '标题\n- point 1\n- point 2'
        t = Topic(content=content)
        self.assertEquals(u'<p>标题\n- point 1\n- point 2</p>\n', t.rendered_content)
    
    def test_render_topic_content_html(self):
        html = '<h2>标题</h2><p>内容</p>'
        t = Topic(html=html, content_type='html')
        self.assertEquals(html, t.rendered_content)
    
    def test_topic_status(self):
        pass
