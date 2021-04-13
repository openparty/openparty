# -*- coding: utf-8 -*-
import re, urllib, hashlib, random, datetime
from urllib.parse import urlencode
from hashlib import sha512 as sha_constructor
from django.db import models
from django.conf import settings
from django.template.loader import render_to_string
from django.db.transaction import atomic
from django.contrib.auth.models import User
from django.core.cache import cache
import logging


ACTIVATION_KEY_PATTERN = re.compile("^[a-f0-9]{40}$")


class MemberManager(models.Manager):
    @atomic
    def create_with_inactive_user(self, email, password, nickname=""):
        def generate_activation_key(email):
            salt = sha_constructor(str(random.random())).hexdigest()[:8]
            activation_key = sha_constructor(salt + email).hexdigest()
            return activation_key

        user = User()
        user.username = email
        user.email = email
        user.set_password(password)
        user.is_active = True
        user.save()

        activation_key = generate_activation_key(email)
        member = self.model(user=user, nickname=nickname, activation_key=activation_key)
        member.save()
        member.send_activation_email()

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
        except Exception as e:
            logging.exception("find_by_email")
            pass
        return None


class Member(models.Model):
    ACTIVATED = "ALREADY_ACTIVATED"

    user = models.OneToOneField(
        User, related_name="profile", verbose_name=u"用户", on_delete=models.CASCADE
    )
    nickname = models.CharField(verbose_name=u"用户名称", max_length=40)
    properties = models.TextField(verbose_name=u"属性", blank=True)
    activation_key = models.CharField(
        verbose_name=u"激活密钥 Activation Key", max_length=40
    )
    twitter_access_token_key = models.CharField(
        u"Twitter OAuth key", blank=True, null=True, max_length=80
    )
    twitter_access_token_secret = models.CharField(
        u"Twitter OAuth secret", blank=True, null=True, max_length=128
    )
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
        default = settings.SITE_URL + "/media/images/default_gravatar.png"
        size = 40
        gravatar_url = "http://www.gravatar.com/avatar.php?"
        gravatar_url += urlencode(
            {
                "gravatar_id": hashlib.md5(
                    self.user.username.encode("utf-8")
                ).hexdigest(),
                "default": default,
                "size": str(size),
            }
        )
        return gravatar_url

    def send_activation_email(self):
        ctx = {
            "activation_key": self.activation_key,
            "expiration_days": settings.ACCOUNT_ACTIVATION_DAYS,
            "site": settings.SITE_URL,
        }

        subject = "[Open Party] 帐号激活"
        message = render_to_string("member/activation_email.txt", ctx)

        self.user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)

    def _generate_pwd_reset_token(self):
        salt = sha_constructor(str(random.random())).hexdigest()[:8]
        token = sha_constructor(salt + self.user.username).hexdigest()
        cache.set("pwd_reset_token:%s" % self.user.id, token, 60 * 60 * 3)
        return token

    def is_pwd_reset_token_expired(self, given_token):
        return not (
            given_token
            and cache.get("pwd_reset_token:%s" % self.user.id, None) == given_token
        )

    def delete_pwd_reset_token(self):
        cache.delete("pwd_reset_token:%s" % self.user.id)

    def send_reset_password_email(self):
        ctx = {
            "activation_key": self._generate_pwd_reset_token(),
            "expiration_days": settings.ACCOUNT_ACTIVATION_DAYS,
            "user_id": self.id,
            "site": settings.SITE_URL,
        }

        subject = "[Open Party] 密码重置"
        message = render_to_string("member/resetpwd_email.txt", ctx)

        self.user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)

    def is_activation_key_expired(self):
        expiration_date = datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS)
        already_joined_longer_than_expiration_days = (
            self.user.date_joined + expiration_date <= datetime.datetime.now()
        )
        return (
            self.activation_key == self.ACTIVATED
            or already_joined_longer_than_expiration_days
        )
