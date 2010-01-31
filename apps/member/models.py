# -*- coding: utf-8 -*-
import urllib, hashlib
from django.db import models

from django.contrib.auth.models import User

class Member(models.Model):
	
	user = models.OneToOneField(User, unique=True, verbose_name=u"用户")
	
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