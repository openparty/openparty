# -*- coding: utf-8 -*-

from django.test import TestCase

class StatusCheckTest(TestCase):
    def statuscheck_indexpage(self):
        response = self.client.get("/")
        #Check the response status
        self.failUnlessEqual(response.status_code, 200)
        #check template usage

    def statuscheck_eventlistpage(self):
        response = self.client.get("/events")
        self.failUnlessEqual(response.status_code, 200)

    def statuscheck_topiclist_page(self):
        response = self.client.get("/topics")
        self.failUnlessEqual(response.status_code, 200)

    def statuscheck_eventdetail_page(self):
        response = self.client.get("/event/1")
        self.failUnlessEqual(response.status_code, 200)
        response = self.client.get("/event/19999")
        self.failUnlessEqual(response.status_code, 200)




