# -*- coding: utf-8 -*-
import urllib, hashlib, random
from django.db import models
from django.conf import settings
from django.utils.hashcompat import sha_constructor
from django.template.loader import render_to_string
from django.db.transaction import commit_on_success
from django.contrib.auth.models import User

import user


class MemberManager(models.Manager):
    @commit_on_success
    def create_with_inactive_user(self, email, password, nickname=''):
        def generate_activation_key(email):
            salt = sha_constructor(str(random.random())).hexdigest()[:8]
            activation_key = sha_constructor(salt+email).hexdigest()
            return activation_key

        user = User()
        user.username = email
        user.email = email
        user.set_password(password)
        user.is_active = False
        user.save()

        activation_key = generate_activation_key(email)
        member = self.model(user=user, nickname=nickname, activation_key=activation_key)
        member.send_activation_email()
        member.save()

        return member


class Member(models.Model):
    ACTIVATED = "ALREADY_ACTIVATED"
    
    user = models.OneToOneField(User, unique=True, verbose_name=u"用户")
    nickname = models.CharField(verbose_name=u'用户名称', max_length=40)
    activation_key = models.CharField(verbose_name=u'激活密钥 Activation Key', max_length=40)

    objects = MemberManager()
    
    def __unicode__(self):
        return self.user.username
    
    @property
    def avatar(self):
        default = 'http://userserve-ak.last.fm/serve/64s/9907065.png'
        size = 40
        gravatar_url = "http://www.gravatar.com/avatar.php?"
        gravatar_url += urllib.urlencode({'gravatar_id':hashlib.md5(self.user.username).hexdigest(),
                                        'default':default, 'size':str(size)})
        return gravatar_url

    def send_activation_email(self):
        ctx = { 'activation_key': self.activation_key,
                'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
                'site': settings.SITE_URL }

        subject = "[Open Party] 帐号激活"
        message = render_to_string('member/activation_email.txt', ctx)

        self.user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)