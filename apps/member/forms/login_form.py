# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import authenticate, login


class LoginForm(forms.Form):
	email = forms.EmailField(label=u'email地址', required=True, widget=forms.TextInput())
	password = forms.CharField(label=u'密码', required=True, widget=forms.PasswordInput(render_value=False))
	remember = forms.BooleanField(label=u'记住登陆信息', help_text=u'如果选择记住登陆信息，会保留登陆信息2周', required = False)
	
	user = None
	
	def clean(self):
		credential = { 'username': self.cleaned_data['email'], 'password': self.cleaned_data['password'] }
		user = authenticate(**credential)
		if user:
			if user.is_active:
				self.user = user
			else:
				raise forms.ValidationError(u'您还没有通过邮件激活帐号，请您登陆邮箱打开链接激活')
		else:
			raise forms.ValidationError(u'您输入的邮件地址与密码不匹配或者帐号还不存在，请您重试或者注册帐号')
		return self.cleaned_data

	def login(self, request):
		if self.is_valid():
			login(request, self.user)
			if "remember" in self.cleaned_data and self.cleaned_data["remember"]:
				request.session.set_expiry(60 * 60 * 24 * 7 * 3)
			else:
				request.session.set_expiry(0)
			return True
		return False
