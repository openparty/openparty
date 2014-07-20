# -*- coding: utf-8 -*-
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.http import (HttpResponse, HttpResponsePermanentRedirect,
                         HttpResponseForbidden, Http404)
from django.shortcuts import redirect, get_object_or_404, get_list_or_404, render
from django.views.generic import ListView
from django import forms

from apps.member.models import Member
from apps.member.forms import ProfileForm

from forms import ArticleForm, EventCheckinForm
from models import Event, Topic, Post
from models import Vote


def index(request):
    topic_list = Topic.objects.all().order_by('-in_event__begin_time', '-accepted', '-total_votes')[:8]
    event_list = Event.objects.past_events().order_by('-begin_time')[:3]
    post_list = Post.objects.all().order_by('-created_at')[:15]
    next_event = Event.objects.next_event()

    ctx = {
        'event_list': event_list,
        'topic_list': topic_list,
        'post_list': post_list,
        'next_event': next_event,
        'tab': 'index',
    }
    return render(request, 'core/index.html', ctx)


class EventList(ListView):
    queryset = Event.objects.all().order_by('-begin_time')
    context_object_name = 'event_list'
    template_name = 'core/event_list.html'

    def get_context_data(self, **kwargs):
        context = super(EventList, self).get_context_data(**kwargs)
        context['tab'] = 'event'
        context['topic_list'] = Topic.objects.all().order_by('-total_votes')
        return context


class TopicList(ListView):
    queryset = Topic.objects.filter(accepted=True) \
        .order_by('-in_event__begin_time', '-accepted', '-total_votes')
    context_object_name = 'topic_list'
    template_name = 'core/topic_list.html'
    paginate_by = 16

    def get_context_data(self, **kwargs):
        context = super(TopicList, self).get_context_data(**kwargs)
        context['tab'] = 'topic'
        return context


def join_event(request):
    if not request.user.is_authenticated():
        messages.info(request, u'对不起，您需要先登录才能报名参加活动，如果没有帐号可以选择<a href="/member/signup">注册</a>')
        return redirect(reverse('login'))

    next_event = Event.objects.next_event()

    if request.method == 'POST':
        form = ProfileForm(request.user, request.POST)
        member = form.save()
        if member:
            next_event.participants.add(member)
            messages.success(request, u'您已经成功报名参加《%s》活动，您是第%s名参加者' % (next_event.name, next_event.participants.count()))
            return redirect('/event/%s' % (next_event.id))
    else:
        try:
            this_user = request.user.get_profile()
        except:
            return redirect(reverse('signup'))

        if not next_event:
            raise Http404

        if this_user in next_event.participants.all():
            success_msg = u'感谢您的参与，您已经成功报名参加了 %s 活动 - 点击<a href="/event/%s">查看活动详情</a>' % (
                next_event.name,
                next_event.id)
            messages.success(request, success_msg)
            return redirect('/event/%s' % (next_event.id))
        else:
            form = ProfileForm(request.user)

    ctx = {
        'form': form,
        'next_event': next_event,
        'tab': 'event',
    }
    return render(request, 'core/join_evnet.html', ctx)


def checkin(request):
    ctx = {'tab': 'event'}
    event = Event.objects.next_event()
    if request.method == 'GET':
        form = EventCheckinForm()
    else:
        form = EventCheckinForm(request.POST)
        try:
            if form.checkin(event):
                ctx['form'] = form
                ctx['event'] = event
                return render(request, 'core/checkin_completed.html', ctx)
        except forms.ValidationError, e:
            for error_message in e.messages:
                messages.error(request, error_message)
    ctx['form'] = form
    ctx['event'] = event
    return render(request, 'core/checkin.html', ctx)


def event(request, id):
    this_event = get_object_or_404(Event, pk=id)
    topics_shown_in = this_event.topic_shown_in.filter(accepted=True)

    ctx = {
        'this_event': this_event,
        'topics_shown_in': topics_shown_in,
        'tab': 'event',
    }
    return render(request, 'core/event.html', ctx)


def topic(request, id):
    this_topic = get_object_or_404(Topic, pk=id)

    is_voted = False
    try:
        vote_thistopic = this_topic.votes.get(user=request.user.get_profile())
        is_voted = True
    except:
        pass

    modified = False
    if this_topic.created != this_topic.last_modified:
        modified = True

    ctx = {
        'this_topic': this_topic,
        'is_voted': is_voted,
        'modified': modified,
        'tab': 'topic',
    }
    return render(request, 'core/topic.html', ctx)


def votes_for_topic(request, id):
    this_topic = get_object_or_404(Topic, pk=id)
    votes_list = this_topic.votes.all().order_by('-id')
    tab = 'topic'
    ctx = {
        'this_topic': this_topic,
        'votes_list': votes_list,
        'tab': tab,
    }
    return render(request, 'core/votes_for_topic.html', ctx)


@login_required
def vote(request, id):

    this_topic = Topic.objects.get(pk=id)

    is_voted = False
    try:
        vote_thistopic = this_topic.votes.get(user=request.user.get_profile())
        is_voted = True
    except:
        pass

    if is_voted is False:
        this_vote = Vote(user=request.user.get_profile())
        # this_topic.votes.add(user = request.user)
        topic_type = ContentType.objects.get_for_model(Topic)
        this_vote.content_type = topic_type
        this_vote.object_id = this_topic.id
        this_vote.save()

    # update vote count
    this_topic.save()

    return redirect(reverse(topic, args=[this_topic.id]))


@login_required
def submit_topic(request):
    if request.method == 'GET':
        form = ArticleForm()
        form.fields['in_event'].queryset = Event.objects.upcoming_events()

        context = {
            'form': form,
            'tab': 'topic',
        }
        return render(request, 'core/submit_topic.html', context)

    if request.method == 'POST':
        form = ArticleForm(request.POST)
        context = {
            'form': form,
            'save_success': False,
        }

        if form.is_valid():
            topic = form.save(commit=False)
            if request.POST['captcha'] == '':
                topic = form.save(commit=False)
                topic.set_author(request.user)
                topic.save()
                topic.send_notification_mail('created')
                context['save_success'] = True
            else:
                return HttpResponseForbidden()

        return render(request, 'core/submit_topic.html', context)


@login_required
def edit_topic(request, id):
    this_topic = get_object_or_404(Topic, pk=id)
    if this_topic.author.user != request.user:
        return redirect(reverse('topic', args=[this_topic.id]))

    if request.method == 'GET':
        context = {
            'form': ArticleForm(instance=this_topic),
            'topic': this_topic,
            'tab': 'topic',
        }
        return render(request, 'core/edit_topic.html', context)

    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=this_topic)
        topic = form.save(commit=False)
        topic.set_author(request.user)
        topic.save()
        topic.send_notification_mail('updated')

        context = {
            'form': form,
            'topic': topic,
            'edit_success': True,
            'tab': 'topic',
        }

        return render(request, 'core/edit_topic.html', context)


def list_post(request):
    all_post = get_list_or_404(Post.objects.order_by('-created_at'), status=Post.post_status.OPEN)
    paginator = Paginator(all_post, 15)
    try:
        page_num = int(request.GET.get('page', '1'))
    except ValueError:
        page_num = 1

    try:
        page = paginator.page(page_num)
    except (EmptyPage, InvalidPage):
        page = paginator.page(paginator.num_pages)

    ctx = {
        'posts': page.object_list,
        'page': page,
        'tab': 'post',
    }
    return render(request, 'core/list_post.html', ctx)


def view_post(request, id):
    post = get_object_or_404(Post, id=id)
    ctx = {
        'post': post,
        'tab': 'post',
    }
    return render(request, 'core/post.html', ctx)


def view_post_by_name(request, name):
    post = get_object_or_404(Post, post_name=name)
    ctx = {
        'post': post,
        'object': post,  # for pingback hook
        'tab': 'post',
    }
    return render(request, 'core/post.html', ctx)


def redirect_wordpress_post(request, year, month, name):
    return redirect(reverse('view_post_by_name', args=[name]))
