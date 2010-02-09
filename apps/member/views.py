# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from openparty.apps.member.forms import LoginForm, SignupForm

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.login(request):
            return HttpResponseRedirect('index')
    else:
        form = LoginForm()
    
    ctx = { 'form': form, }
    return render_to_response('member/login.html', ctx, context_instance=RequestContext(request))

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