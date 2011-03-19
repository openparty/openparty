# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.core.validators import validate_email
from apps.member.models import Member


class RequestResetPasswordForm(forms.Form):
    email = forms.EmailField(label=u'email', required=True, widget=forms.TextInput(attrs={'tabindex': '1'}))
    
    user = None
    
    def clean_email(self):
        email=self.cleaned_data.get('email','')
        validate_email(email)
        return email
    
    def clean(self):
        super(RequestResetPasswordForm,self).clean()
        usermail = self.cleaned_data.get('email','')
        user = Member.objects.get(user__email=usermail).user
        if not user:
            raise forms.ValidationError(u'您输入的邮件地址与密码不匹配或者帐号还不存在，请您重试或者注册帐号')
        return self.cleaned_data
