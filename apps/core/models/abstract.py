# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class Base(models.Model):
    name = models.CharField(max_length=255, blank=False)

    created = models.DateTimeField(auto_now_add=True, auto_now=True, blank=True, null=True)

    last_modified = models.DateTimeField(auto_now_add=True, auto_now=True, blank=True, null=True)
    last_modified_by = models.ForeignKey(User, related_name='%(class)s_last_modified')

    #aggrgated
    total_votes = models.PositiveIntegerField(default=0)
    total_favourites = models.PositiveIntegerField(default=0, editable=False)

    class Meta:
        abstract = True
        app_label = 'core'

class Attachable(models.Model):
    conntent_type = models.ForeignKey(ContentType, limit_choices_to = {'model__in': ('topic', 'event', 'comment')})
    object_id = models.PositiveIntegerField()
    item = generic.GenericForeignKey('content_type', 'object_id')

    created = models.DateTimeField("创建日期",auto_now_add=True) 

    # denorm 
    item_raw = models.TextField('item raw',blank=True) 
    user_raw = models.TextField('user raw',blank=True) 

    class Meta:
        abstract = True
        app_label = 'core'


