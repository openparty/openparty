# -*- coding: utf-8 -*-
import re
from django import forms
from django.contrib.auth.models import User
from openparty.apps.member.models import Member

class SignupForm(forms.Form):
    email = forms.EmailField(label=u'email地址', required=True, widget=forms.TextInput())
    nickname = forms.CharField(label=u'昵称', required=False, max_length=30, widget=forms.TextInput())
    
    password1 = forms.CharField(label=u'密码', required=True, widget=forms.PasswordInput(render_value=False))
    password2 = forms.CharField(label=u'重复密码', widget=forms.PasswordInput(render_value=False))
    
    def clean_nickname(self):
        nickname = self.cleaned_data['nickname'].strip()
        if nickname and (not re.compile(ur'^[\w|\u2E80-\u9FFF]+$').search(nickname)):
            raise forms.ValidationError(u'昵称“%s”名非法，昵称目前仅允许使用中英文字数字和下划线' % nickname)
        return nickname
    
    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        try:
            # 每个Member对应一个User，但是允许后台User不对应Member
            User.objects.get(username__iexact=email) 
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(u'已经有用户使用“%s”注册了用户，请您确认邮件是否拼写错误' % email)
        return email
    
    def clean_password1(self):
        password = self.cleaned_data['password1'].strip()
        if not password:
            raise forms.ValidationError(u'对不起，密码不能为空')
        return password
    
    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(u'您所输入的两个密码不一致，请您重新输入')
        return self.cleaned_data
    
    def save(self):
        if not self.is_valid():
            return False
        email = self.cleaned_data['email']
        nickname = self.cleaned_data['nickname']
        password = self.cleaned_data['password1']
        
        
        user = User()
        user.username = email
        user.email = email
        user.set_password(password)
        user.is_active = False
        user.save()
        
        member = Member(user=user)
        member.save()
        return member
