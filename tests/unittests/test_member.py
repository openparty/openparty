# -*- coding: utf-8 -*-
import unittest
from openparty.apps.member.models import Member
from openparty.apps.member.forms import SignupForm, LoginForm
import openparty.tests.unittests.test_helper as helper

class MemberTest(unittest.TestCase):
    def test_dummy_function(self):
        self.assertTrue(True)