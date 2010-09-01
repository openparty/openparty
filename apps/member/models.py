# -*- coding: utf-8 -*-
import re, urllib, hashlib, random, datetime
from django.db import models
from django.conf import settings
from django.utils.hashcompat import sha_constructor
from django.template.loader import render_to_string
from django.db.transaction import commit_on_success
from django.contrib.auth.models import User

import user

ACTIVATION_KEY_PATTERN = re.compile('^[a-f0-9]{40}$')

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
    
    def find_by_activation_key(self, activation_key):
        if ACTIVATION_KEY_PATTERN.search(activation_key):
            try:
                member = self.get(activation_key=activation_key)
            except self.model.DoesNotExist:
                return False
            if not member.is_activation_key_expired():
                user = member.user
                user.is_active = True
                user.save()
                member.activation_key = self.model.ACTIVATED
                member.save()
                return member
        return False
    
    def find_by_email(self, email):
        try:
            user = User.objects.get(username=email)
            if user:
                return self.get(user=user)
        except User.DoesNotExist:
            pass
        except self.DoesNotExist:
            pass
        return None


class Member(models.Model):
    ACTIVATED = "ALREADY_ACTIVATED"
    
    user = models.OneToOneField(User, unique=True, verbose_name=u"用户")
    nickname = models.CharField(verbose_name=u'用户名称', max_length=40)
    properties = models.TextField(verbose_name=u'属性', blank=True)
    activation_key = models.CharField(verbose_name=u'激活密钥 Activation Key', max_length=40)
    twitter_access_token_key = models.CharField(u'Twitter OAuth key', blank=True, null=True, max_length=80)
    twitter_access_token_secret = models.CharField(u'Twitter OAuth secret', blank=True, null=True, max_length=128)
    twitter_enabled = models.BooleanField(default=False)

    objects = MemberManager()
    
    def __unicode__(self):
        return self.user.username
    
    @property
    def display_name(self):
        if self.nickname:
            return self.nickname
        else:
            return self.user.username
    
    @property
    def avatar(self):
        default = 'http://app.beijing-open-party.org/media/images/default_gravatar.png'
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
    
    def is_activation_key_expired(self):
        expiration_date = datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS)
        already_joined_longer_than_expiration_days = (self.user.date_joined + expiration_date <= datetime.datetime.now())
        return self.activation_key == self.ACTIVATED or already_joined_longer_than_expiration_days
