# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from apps.member.models import Member


class ChangePasswordForm(forms.Form):
    oldpassword = forms.CharField(
        label=u"旧密码",
        required=True,
        widget=forms.PasswordInput(render_value=False, attrs={"tabindex": "1"}),
    )
    password1 = forms.CharField(
        label=u"新密码",
        required=True,
        widget=forms.PasswordInput(render_value=False, attrs={"tabindex": "2"}),
    )
    password2 = forms.CharField(
        label=u"重复密码",
        required=True,
        widget=forms.PasswordInput(render_value=False, attrs={"tabindex": "3"}),
    )

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean_oldpassword(self):
        if not self.user.check_password(self.cleaned_data.get("oldpassword")):
            raise forms.ValidationError(u"您填写的旧密码不正确呀，要不您再试试（注意大小写）")
        return self.cleaned_data["oldpassword"]

    def clean_password1(self):
        password = self.cleaned_data["password1"].strip()
        if not password:
            raise forms.ValidationError(u"对不起，密码不能为空")
        return password

    def clean(self):
        if "password1" in self.cleaned_data and "password2" in self.cleaned_data:
            if self.cleaned_data["password1"] != self.cleaned_data["password2"]:
                raise forms.ValidationError(u"您所输入的两个密码不一致，请您重新输入")
        return self.cleaned_data

    def save(self):
        if not self.is_valid():
            return False
        password = self.cleaned_data["password1"]
        self.user.set_password(password)
        self.user.save()
        return True
