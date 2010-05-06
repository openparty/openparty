# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404

from apps.member.models import Member
from apps.member.forms import ProfileForm

from forms import ArticleForm
from models import Event, Topic
from models import Vote


def index(request):
    event_list = Event.objects.all().order_by('-begin_time')[:5]
    topic_list = Topic.objects.all().order_by('-total_votes')[:5]

    event_list = Event.past.all()

    next_event = Event.objects.next_event()

    ctx = {
        'request': request,
        'event_list': event_list,
        'topic_list': topic_list,
        'next_event': next_event, 
    }
    return render_to_response('core/index.html', ctx, context_instance=RequestContext(request))

def event_list(request):
    event_list = Event.objects.all().order_by('-begin_time')
    topic_list = Topic.objects.all().order_by('-total_votes')
    return render_to_response('core/event_list.html', locals(), context_instance=RequestContext(request))

def topic_list(request):
    topic_list = Topic.objects.all().order_by('-total_votes').order_by('-in_event__begin_time')
    #需注意排序顺序
    return render_to_response('core/topic_list.html', locals(), context_instance=RequestContext(request))

def join_event(request):
    if not request.user.is_authenticated():
        messages.info(request, u'对不起，您需要先登录才能报名参加活动，如果没有帐号可以选择<a href="/signup">注册</a>')
        return redirect('/login')

    if request.method == 'POST':
        form = ProfileForm(request.user, request.POST)
        member = form.save()
        if member:
            next_event = Event.objects.next_event()
            next_event.participants.add(member)
            messages.success(request, u'您已经成功报名参加《%s》活动，您是第%s名参加者' % (next_event.name, next_event.participants.count()))
            return redirect('/')
    else:
        try:
            this_user = Member.objects.get(user = request.user)
        except:
            return redirect('/signup')
        
        next_event = Event.objects.next_event()
        if this_user in next_event.participants.all():
            messages.success(request, u'感谢您的参与，您已经成功报名参加了 %s 活动 - 点击<a href="/event/%s">查看活动详情</a>' % (next_event.name, next_event.id))
            return redirect('/event/%s' % (next_event.id))
        else: 
            form = ProfileForm(request.user)
            next_event = Event.objects.next_event()

    ctx = { 'form': form, 'next_event': next_event, 'request': request, }
    return render_to_response('core/join_evnet.html', ctx, context_instance=RequestContext(request))

def event(request, id):
    this_event = get_object_or_404(Event, pk = id)
    topics_shown_in = this_event.topic_shown_in.filter(accepted=True)
    return render_to_response('core/event.html', locals(), context_instance=RequestContext(request))

def topic(request, id):
    this_topic = get_object_or_404(Topic, pk = id)

    if this_topic.is_arranged:
        can_vote = True 
    else:
        can_vote = False

    is_voted = False
    try:
        vote_thistopic = this_topic.votes.get(user = Member.objects.get(user=request.user))
        is_voted = True
    except:
        pass

    modified = False
    if this_topic.created != this_topic.last_modified:
        modified = True

    return render_to_response('core/topic.html', locals(), context_instance=RequestContext(request))

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
    
    return HttpResponseRedirect("/")

@login_required
def submit_topic(request):
    if request.method == 'GET':
        form = ArticleForm()
        form.fields['in_event'].queryset = Event.upcoming.all()

        context = {'form': form,
                'request': request,
                }
        return render_to_response('core/submit_topic.html',
                                    context,
                                    context_instance=RequestContext(request))

    if request.method == 'POST':
        form = ArticleForm(request.POST)
        topic = form.save(commit=False)
        topic.set_author(request.user)
        topic.save()
        
        context = {
            'request': request,
            'form': form,
            'topic': topic,
            'save_success': True
        }
        
        return render_to_response('core/submit_topic.html',
                                    context,
                                    context_instance=RequestContext(request))
@login_required
def edit_topic(request, id):
    try:
        this_topic = Topic.objects.get(pk = id)
    except:
        #TODO redirect to an error page
        return HttpResponseRedirect("/")

    if request.method == 'GET':
        context = {
                    'form': ArticleForm(instance = this_topic)
                  }
        return render_to_response('core/edit_topic.html', 
                                    context,
                                    context_instance=RequestContext(request))

    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=this_topic)
        topic = form.save(commit=False)
        topic.set_author(request.user)
        topic.save()

        context = {
            'request': request,
            'form': form,
            'topic': topic,
            'edit_success': True
        }
        
        return render_to_response('core/edit_topic.html',
                                    context,
                                    context_instance=RequestContext(request))
