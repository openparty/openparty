# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import logout as auth_logout

from openparty.apps.member.forms import LoginForm, SignupForm
from openparty.apps.member.models import Member

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.login(request):
            return HttpResponseRedirect('index')
    else:
        form = LoginForm()

    ctx = { 'form': form, }
    return render_to_response('member/login.html', ctx, context_instance=RequestContext(request))

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.save():
            ctx = { 'email': form.cleaned_data['email'], }
            return render_to_response('member/verification_sent.html', ctx, context_instance=RequestContext(request))
    else:
        form = SignupForm()

    ctx = { 'form': form, }
    return render_to_response('member/signup.html', ctx, context_instance=RequestContext(request))

def activate(request, activation_key):
    activating_member = Member.objects.find_by_activation_key(activation_key)
    if activating_member:
        messages.success(request, u'您的帐号已经成功激活，请尝试登录吧')
    else:
        messages.error(request, u'对不起，您所的激活号码已经过期或者根本就不存在？')
    return redirect('/login')