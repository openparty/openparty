# -*- coding: utf-8 -*-
from django.shortcuts import redirect, render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import FormView
from django.http import Http404

from apps.member.forms import LoginForm, SignupForm, ChangePasswordForm, ProfileForm, RequestResetPasswordForm, ResetPasswordForm
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
    return render(request, 'member/login.html', ctx)

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')

def signup(request):
    if request.method == 'POST' and request.POST['captcha'] == '':
        form = SignupForm(request.POST)
        if form.save():
            ctx = { 'email': form.cleaned_data['email'], }
            return render(request, 'member/verification_sent.html', ctx)
    else:
        form = SignupForm()

    ctx = { 'form': form,  }
    return render(request, 'member/signup.html', ctx)

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
    return render(request, 'member/change_password.html', ctx)

class MemberRequestResetPasswordView(FormView):
    form_class = RequestResetPasswordForm
    template_name = 'member/request_reset_password.html'

    def form_valid(self, form):
        this_member = Member.objects.get(user__email=form.cleaned_data['email'])
        this_member.send_reset_password_email()
        return super(MemberRequestResetPasswordView, self).form_valid(form)

    def get_success_url(self):
        return reverse('member_request_reset_pwd_done')

class MemberRequestResetPasswordDone(TemplateView):
    template_name = 'member/request_reset_password_done.html'

def reset_password(request, user_id, pwd_reset_token):
    try:
        this_member = Member.objects.get(id=user_id)
    except Member.DoesNotExist:
        raise Http404
    token = pwd_reset_token
    if request.method == 'POST' and not this_member.is_pwd_reset_token_expired(token):
        form = ResetPasswordForm(this_member.user, request.POST)
        if form.save():
            messages.success(request, u'您的密码已经修改')
            this_member.delete_pwd_reset_token()
            return redirect('/')
    elif not this_member.is_pwd_reset_token_expired(token):
        form = ResetPasswordForm(request)
        ctx = { 'form': form,  }
    else:
        ctx = { 'status': 'failed' }
    return render(request, 'member/reset_password.html', ctx)

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
    return render(request, 'member/update_profile.html', ctx)


class MemberProfileView(DetailView):

    context_object_name = "member"
    model = Member

    def get_queryset(self, **kwargs):
        queryset = super(MemberProfileView, self).get_queryset(**kwargs)
        return queryset.select_related()
