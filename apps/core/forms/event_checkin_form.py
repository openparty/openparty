# -*- coding: utf-8 -*-
from django import forms
from django.core.validators import validate_email
from apps.member.models import Member


class EventCheckinForm(forms.Form):
    email = forms.EmailField(label=u'请填写您注册使用的Email', required=True, widget=forms.TextInput(attrs={'tabindex': '1'}))
    member = None
    
    def clean_email(self):
        email=self.cleaned_data.get('email','')
        validate_email(email)
        return email
    
    def clean(self):
        super(EventCheckinForm, self).clean()
        email = self.cleaned_data.get('email','')
        member = Member.objects.find_by_email(email)
        if member:
            self.member = member
        else:
            raise forms.ValidationError(u'您输入的邮件地址与密码不匹配或者帐号还不存在，请您重试')
        return self.cleaned_data

    def checkin(self, event):
        if self.is_valid():
            if self.member in event.appearances.all():
                raise forms.ValidationError(u'嘿，您已经签过到了，请下一位签到吧！')
            else:
                print(self.member)
                print(self.member.id)
                event.appearances.add(self.member)
            return True
        else:
            return False
