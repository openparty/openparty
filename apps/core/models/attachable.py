# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


class Attachable(models.Model):
    content_type = models.ForeignKey(ContentType, limit_choices_to = {'model__in': ('topic', 'event', 'comment')})
    object_id = models.PositiveIntegerField()
    item = generic.GenericForeignKey('content_type', 'object_id')

    created = models.DateTimeField("创建日期",auto_now_add=True)

    # denorm
    item_raw = models.TextField('item raw',blank=True)
    user_raw = models.TextField('user raw',blank=True)

    class Meta:
        abstract = True
        app_label = 'core'

