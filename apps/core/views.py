# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.contrib.auth.models import User

from models import Event, Topic

def render(template_name, template_values, request):
    """render the template"""
    return render_to_response(template_name, template_values, context_instance=RequestContext(request))

def index(request):
    event_list = Event.objects.all().order_by('-datetime_begin')
    topic_list = Topic.objects.all().order_by('-total_votes')
    return render('core/index.html', locals(), request)
    #return render_to_response('index.html', {}, context_instance=RequestContext(request))

def event_list(request):
    event_list = Event.objects.all().order_by('-datetime_begin')
    topic_list = Topic.objects.all().order_by('-total_votes')
    return render('core/event_list.html', locals(), request)

def topic_list(request):
    topic_list = Topic.objects.all().order_by('-total_votes').order_by('-shown_in_event__datetime_begin')
    #需注意排序顺序
    return render('core/topic_list.html', locals(), request)

def event(request, id):
    this_event = Event.objects.get(pk = id)
    return render('core/event.html', locals(), request)
