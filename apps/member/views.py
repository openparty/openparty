# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView

from apps.member.forms import LoginForm, SignupForm, ChangePasswordForm, ProfileForm
from apps.member.models import Member
from django.core.urlresolvers import reverse

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.login(request):
            next = request.GET.get("next", "")
            if next:
                return redirect(next)
            return redirect('/')
    else:
        form = LoginForm()

    ctx = { 'form': form,  }
    return render_to_response('member/login.html', ctx, context_instance=RequestContext(request))

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.save():
            ctx = { 'email': form.cleaned_data['email'], }
            return render_to_response('member/verification_sent.html', ctx,
                context_instance=RequestContext(request))
    else:
        form = SignupForm()

    ctx = { 'form': form,  }
    return render_to_response('member/signup.html', ctx, context_instance=RequestContext(request))

def activate(request, activation_key):
    activating_member = Member.objects.find_by_activation_key(activation_key)
    if activating_member:
        messages.success(request, u'您的帐号已经成功激活，请尝试登录吧')
    else:
        messages.error(request, u'对不起，您所的激活号码已经过期或者根本就不存在？')
    return redirect(reverse('login'))

@login_required
def change_password(request):
    if request.method == 'POST' and request.user.is_authenticated():
        form = ChangePasswordForm(request.user, request.POST)
        if form.save():
            messages.success(request, u'您的密码已经修改')
            return redirect('/')
    else:
        form = ChangePasswordForm(request)
    ctx = { 'form': form,  }
    return render_to_response('member/change_password.html', ctx,
        context_instance=RequestContext(request))

@login_required
def update_profile(request):
    if request.method == 'POST' and request.user.is_authenticated():
        form = ProfileForm(request.user, request.POST)
        if form.save():
            messages.success(request, u'您的个人信息已经修改')
            return redirect('/')
    else:
        form = ProfileForm(request.user)
    ctx = { 'form': form,  }
    return render_to_response('member/update_profile.html', ctx,
        context_instance=RequestContext(request))


class MemberProfileView(DetailView):

    context_object_name = "member"
    model = Member

    def get_queryset(self, **kwargs):
        queryset = super(MemberProfileView, self).get_queryset(**kwargs)
        return queryset.select_related()
