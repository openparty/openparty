# -*- coding: utf-8 -*-
from django.test import TestCase
from openparty.apps.member.forms import SignupForm

class MemberTest(TestCase):
	def test_save_member_though_form(self):
			form = SignupForm({ 'email': 'some@domain.com', 'password1': '1', 'password2': '1' })
			member = form.save()
			self.assertTrue(member.id)

	def test_save_member_though_form_with_nickname(self):
		form = SignupForm({ 'email': 'some@domain.com', 'nickname': u'田乐', 'password1': '1', 'password2': '1' })
		member = form.save()
		print form.errors
		self.assertTrue(member.id)

	def test_save_member_should_show_error_when_password_not_matching(self):
		form = SignupForm({ 'email': 'some@domain.com', 'password1': '1', 'password2': '2' })
		self.assertFalse(form.save())
		self.assertEquals(1, len(form.errors))

	def test_save_member_should_show_error_when_email_is_not_valid(self):
		form = SignupForm({ 'email': 'domain.com', 'password1': '1', 'password2': '1' })
		self.assertFalse(form.save())
		self.assertEquals(1, len(form.errors))

	def test_save_member_should_show_error_when_usernick_valid(self):
		form = SignupForm({ 'email': 'domain.com', 'password1': '1', 'nickname': '123456', 'password2': '1' })
		self.assertFalse(form.save())
		self.assertEquals(1, len(form.errors))
		form = SignupForm({ 'email': 'some@domain.com', 'password1': '1', 'nickname': 'Bei Jing', 'password2': '1' })
		self.assertFalse(form.save())
		self.assertEquals(1, len(form.errors))
