# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.contrib.auth.models import User

from models import Event, Topic
from models import Vote

def render(template_name, template_values, request):
    """render the template"""
    return render_to_response(template_name, template_values, context_instance=RequestContext(request))

def index(request):
    event_list = Event.objects.all().order_by('-datetime_begin')
    if event_list[0].is_upcoming == True:
        #有即将开始的活动
        upcoming_topic_list = Topic.objects.filter(in_event=event_list[0]).order_by('-total_votes')[:5]
        #首页优先显示即将开始的活动话题
        if len(upcoming_topic_list) == 0:
            #如果即将开始的活动还没有话题加入，那么根据投票显示以往的热门话题
            topic_list = Topic.objects.all().order_by('-total_votes')[:5]
        else:
            topic_list = upcoming_topic_list
    return render('core/index.html', locals(), request)

def event_list(request):
    event_list = Event.objects.all().order_by('-datetime_begin')
    topic_list = Topic.objects.all().order_by('-total_votes')
    return render('core/event_list.html', locals(), request)

def topic_list(request):
    topic_list = Topic.objects.all().order_by('-total_votes').order_by('-in_event__datetime_begin')
    #需注意排序顺序
    return render('core/topic_list.html', locals(), request)

def event(request, id):
    this_event = Event.objects.get(pk = id)
    return render('core/event.html', locals(), request)

def topic(request, id):
    this_topic = Topic.objects.get(pk = id)

    #vote_thistopic = Vote.objects.get(user = request.user, item = this_topic)
    vote_thistopic = this_topic.votes.get(user = request.user)
    is_voted = False
    try:
        #vote_thistopic = Vote.objects.get(user = request.user, item = this_topic)
        vote_thistopic = this_topic.votes.get(user = request.user)
        is_voted = True
    except:
        pass


    return render('core/topic.html', locals(), request)
