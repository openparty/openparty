# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import authenticate, login
from django.core.validators import validate_email


class LoginForm(forms.Form):
    email = forms.EmailField(
        label=u"email", required=True, widget=forms.TextInput(attrs={"tabindex": "1"})
    )
    password = forms.CharField(
        label=u"密码",
        required=True,
        widget=forms.PasswordInput(render_value=False, attrs={"tabindex": "2"}),
    )
    remember = forms.BooleanField(
        label=u"记住登录信息",
        help_text=u"如果选择记住登录信息，会保留登录信息2周",
        required=False,
        widget=forms.CheckboxInput(attrs={"tabindex": "3"}),
    )

    user = None

    def clean_email(self):
        email = self.cleaned_data.get("email", "")
        validate_email(email)
        return email

    def clean(self):
        super(LoginForm, self).clean()
        credential = {
            "username": self.cleaned_data.get("email", ""),
            "password": self.cleaned_data.get("password", ""),
        }
        user = authenticate(**credential)
        if user:
            if user.is_active:
                self.user = user
            else:
                raise forms.ValidationError(u"您还没有通过邮件激活帐号，请您登录邮箱打开链接激活")
        else:
            raise forms.ValidationError(u"您输入的邮件地址与密码不匹配或者帐号还不存在，请您重试或者注册帐号")
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
