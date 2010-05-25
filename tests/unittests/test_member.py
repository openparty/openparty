# -*- coding: utf-8 -*-
import unittest
from apps.member.models import Member
from apps.member.forms import SignupForm, LoginForm
import tests.unittests.test_helper as helper

class MemberTest(unittest.TestCase):
    def test_dummy_function(self):
        self.assertTrue(True)