# -*- coding: utf-8 -*-
import unittest

from openparty.apps.core.models import Topic

class TopicTest(unittest.TestCase):
    def test_topic_summary(self):
        content = '''软件需求遇到的最大问题是什么？基本上都是沟通和交流的相关问题需求从哪里来：客户（市场）、用户 我们需要确定的是：谁是用户？当前业务流程情况？业务目标是什么？ 项目需求确定中遇到的最大问题是什么？需求文档驱动的过程不堪重负 查看更多'''
        t = Topic(content=content)
        self.assertEquals(u'软件需求遇到的最大问题是什么？...', t.summary)
