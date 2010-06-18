# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django import forms

from apps.member.models import Member
from apps.member.forms import ProfileForm

from forms import ArticleForm, EventCheckinForm
from models import Event, Topic
from models import Vote
from django.core.urlresolvers import reverse

def index(request):
    event_list = Event.objects.all().order_by('-begin_time')[:5]
    topic_list = Topic.objects.all().order_by('-total_votes')[:5]

    event_list = Event.past.all()

    next_event = Event.objects.next_event()

    ctx = {
        'event_list': event_list,
        'topic_list': topic_list,
        'next_event': next_event, 
        'tab': 'index',
    }
    return render_to_response('core/index.html', ctx, context_instance=RequestContext(request))

def event_list(request):
    event_list = Event.objects.all().order_by('-begin_time')
    topic_list = Topic.objects.all().order_by('-total_votes')
    
    ctx = {
        'event_list': event_list,
        'topic_list': topic_list,
        'tab': 'event',
    }
    return render_to_response('core/event_list.html', ctx, context_instance=RequestContext(request))

def topic_list(request):
    topic_list = Topic.objects.all().order_by('-in_event__begin_time','-accepted', '-total_votes')
    #需注意排序顺序
    
    ctx = {
        'topic_list': topic_list,
        'tab': 'topic',
    }
    return render_to_response('core/topic_list.html', ctx, context_instance=RequestContext(request))

def join_event(request):
    if not request.user.is_authenticated():
        messages.info(request, u'对不起，您需要先登录才能报名参加活动，如果没有帐号可以选择<a href="/member/signup">注册</a>')
        return redirect(reverse('login'))

    if request.method == 'POST':
        form = ProfileForm(request.user, request.POST)
        member = form.save()
        if member:
            next_event = Event.objects.next_event()
            next_event.participants.add(member)
            messages.success(request, u'您已经成功报名参加《%s》活动，您是第%s名参加者' % (next_event.name, next_event.participants.count()))
            return redirect('/event/%s' % (next_event.id))
    else:
        try:
            this_user = Member.objects.get(user = request.user)
        except:
            return redirect(reverse('signup'))
        
        next_event = Event.objects.next_event()
        if this_user in next_event.participants.all():
            messages.success(request, u'感谢您的参与，您已经成功报名参加了 %s 活动 - 点击<a href="/event/%s">查看活动详情</a>' % (next_event.name, next_event.id))
            return redirect('/event/%s' % (next_event.id))
        else: 
            form = ProfileForm(request.user)
            next_event = Event.objects.next_event()

    ctx = { 'form': form,
            'next_event': next_event,
            'tab': 'event',
          }
    return render_to_response('core/join_evnet.html', ctx, context_instance=RequestContext(request))

def checkin(request):
    ctx = {'tab': 'event'}
    if request.user.is_staff:
        event = Event.objects.next_event()
        if request.method == 'GET':
            form = EventCheckinForm()
        else:
            form = EventCheckinForm(request.POST)
            try:
                if form.checkin(event):
                    messages.success(request, u'您已经成功在现场签到了！')
            except forms.ValidationError, e:
                for error_message in e.messages:
                    messages.error(request, error_message)
        ctx['form'] = form
        ctx['event'] = event
    else:
        messages.error(request, u'您需要以管理员身份登录访问现场登录页面')
    return render_to_response('core/checkin.html', ctx, context_instance=RequestContext(request))

def event(request, id):
    this_event = get_object_or_404(Event, pk = id)
    topics_shown_in = this_event.topic_shown_in.filter(accepted=True)
    
    ctx = {
        'this_event': this_event,
        'topics_shown_in': topics_shown_in,
        'tab': 'event',
    }
    return render_to_response('core/event.html', ctx, context_instance=RequestContext(request))

def topic(request, id):
    this_topic = get_object_or_404(Topic, pk = id)

    is_voted = False
    try:
        vote_thistopic = this_topic.votes.get(user = Member.objects.get(user=request.user))
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
    return render_to_response('core/topic.html', ctx, context_instance=RequestContext(request))

def votes_for_topic(request, id):
    this_topic = get_object_or_404(Topic, pk = id)
    votes_list = this_topic.votes.all().order_by('-id')
    tab = 'topic'
    ctx = {
        'this_topic': this_topic,
        'votes_list': votes_list,
        'tab': tab,
    }
    return render_to_response('core/votes_for_topic.html', ctx, context_instance=RequestContext(request))

@login_required
def vote(request, id):

    this_topic = Topic.objects.get(pk = id)
    
    is_voted = False
    try:
        vote_thistopic = this_topic.votes.get(user = Member.objects.get(user = request.user))
        is_voted = True
    except:
        pass

    if is_voted == False:
        this_vote = Vote(user = Member.objects.get(user = request.user))
        #this_topic.votes.add(user = request.user)
        topic_type = ContentType.objects.get_for_model(Topic)
        this_vote.content_type=topic_type
        this_vote.object_id=this_topic.id
        this_vote.save()


    #update vote count
    this_topic.save()
    
    return HttpResponseRedirect(reverse(topic, args=[this_topic.id]))

@login_required
def submit_topic(request):
    if request.method == 'GET':
        form = ArticleForm()
        form.fields['in_event'].queryset = Event.upcoming.all()

        context = {'form': form,
                   'tab': 'topic',
                }
        return render_to_response('core/submit_topic.html',
                                    context,
                                    context_instance=RequestContext(request))

    if request.method == 'POST':
        form = ArticleForm(request.POST)
        topic = form.save(commit=False)
        topic.set_author(request.user)
        topic.save()
        topic.send_notification_mail('created')
        
        context = {
            'form': form,
            'topic': topic,
            'save_success': True
        }
        
        return render_to_response('core/submit_topic.html',
                                    context,
                                    context_instance=RequestContext(request))
@login_required
def edit_topic(request, id):

    this_topic = get_object_or_404(Topic, pk = id)
    if this_topic.author.user != request.user:
        return HttpResponseRedirect(reverse('topic', args=[this_topic.id]))

    if request.method == 'GET':
        context = {
                    'form': ArticleForm(instance = this_topic),
                    'topic': this_topic,
                    'tab': 'topic',
                  }
        return render_to_response('core/edit_topic.html', 
                                    context,
                                    context_instance=RequestContext(request))

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
        
        return render_to_response('core/edit_topic.html',
                                    context,
                                    context_instance=RequestContext(request))

