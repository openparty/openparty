# -*- coding: utf-8 -*-
from django.test import TestCase
from django.urls import reverse
from django.core.cache import cache
from django.contrib.sites.models import Site
from django.contrib.auth.models import User

from apps.member.models import Member
from apps.member.forms import SignupForm, LoginForm
from apps.core.models import Event, Topic
import apps.member.test_helper as helper

from datetime import datetime

class MemberTest(TestCase):
    def test_save_member_though_form(self):
        form = SignupForm({ 'email': 'some@domain.com', 'password1': '1', 'password2': '1' })
        member = form.save()
        self.assertTrue(isinstance(member, Member))
        self.assertTrue(member.user.id)

    def test_signup_member_should_login_status(self):
        response = self.client.get('/member/signup')
        assert 'password1' in response.content
        assert 'password2' in response.content
        response = self.client.post('/member/signup', {'email': 'some@domain.com',
                                                  'password1': '1',
                                                  'password2': '1',
                                                  'captcha': ''})
        assert 'some@domain.com' in response.content
        assert '注册确认信已发送' in response.content

    def test_save_member_though_form_with_nickname(self):
        form = SignupForm({ 'email': 'some@domain.com', 'nickname': u'田乐', 'password1': '1', 'password2': '1' })
        member = form.save()
        self.assertTrue(member.user.id)

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

    def test_login(self):
        helper.create_user()
        response = self.client.post(reverse('login'), {'email': 'tin@domain.com', 'password': '123'})
        self.assertRedirects(response, '/')

    def test_login_should_failed_when_password_is_wrong(self):
        helper.create_user()
        response = self.client.post(reverse('login'), {'email': 'tin@domain.com', 'password': 'wrong-password'})
        self.assertFormError(response, 'form', '', u'您输入的邮件地址与密码不匹配或者帐号还不存在，请您重试或者注册帐号')

    # 暂时注释掉，因为邮件服务器总有问题，所以我们选择不需要邮件激活
    # def test_login_should_failed_before_activate(self):
    #         helper.create_user(activate=False)
    #         response = self.client.post(reverse('login'), {'email': 'tin@domain.com', 'password': '123'})
    #         self.assertFormError(response, 'form', '', u'您还没有通过邮件激活帐号，请您登录邮箱打开链接激活')

    def test_avatar_of_member(self):
        import settings
        member = helper.create_user()
        user = member.user
        self.assertEquals('http://www.gravatar.com/avatar.php?default=http%3A%2F%2F' + settings.SITE_URL[len("http://"):] + '%2Fmedia%2Fimages%2Fdefault_gravatar.png&size=40&gravatar_id=ea746490cff50b7d53bf78a11c86815a', user.profile.avatar)

    def test_find_member_by_email(self):
        member = helper.create_user()
        user = member.user
        found = Member.objects.find_by_email(user.email)
        self.assertEquals(member, found)

    def test_find_member_by_none_existing_email(self):
        not_found = Member.objects.find_by_email('iamnotexisting@gmail.com')
        self.assertFalse(not_found)

    def test_reset_password(self):
        member = helper.create_user()
        response = self.client.post('/member/request_reset_password', {'email': member.user.email})
        self.assertRedirects(response, '/member/request_reset_password_done')

        token = cache.get('pwd_reset_token:%s' % member.id)
        assert token is not None

        reset_password_url = '/member/reset_password/%s/%s/' % (member.id, token)
        response = self.client.get(reset_password_url)
        assert '新密码' in response.content
        assert '重复密码' in response.content

        response = self.client.post(reset_password_url, {'password1': '1', 'password2': '1'}, follow=True)
        self.assertRedirects(response, '/')
        assert '您的密码已经修改' in response.content


class StatusTest(TestCase):
    def setUp(self):
        new_user = User.objects.create(username="tester", password="tester")
        new_user.save()
        self.client.login(username="tester", passsword="tester")
        new_member = Member.objects.create(user=new_user, nickname="tester")
        new_member.save()
        new_event = Event.objects.create(name="test event 01", description="xxx", content="xxx", begin_time = datetime.now(), end_time = datetime.now(), last_modified_by=new_member)
        new_event.save()
        new_topic = Topic.objects.create(name="test topic 01", description="xxx", content="xxx", author=new_member, last_modified_by=new_member)
        new_topic.save()

    def test_statuscheck_member_profile(self):
        response = self.client.get(reverse('member_profile', kwargs={"pk":1}))
        self.failUnlessEqual(response.status_code, 200)
