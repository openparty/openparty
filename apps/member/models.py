# -*- coding: utf-8 -*-
from django.db import models

from django.contrib.auth.models import User

class Member(models.Model):
	
	user = models.OneToOneField(User, unique=True, verbose_name=u"用户")
	
	def __unicode__(self):
		return self.user.username