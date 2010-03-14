# -*- coding: utf-8 -*-
from django.db import models

from openparty.apps.member.models import Member

class Base(models.Model):
    name = models.CharField(max_length=255, blank=False)

    created = models.DateTimeField(auto_now_add=True, auto_now=True, blank=True, null=True)

    last_modified = models.DateTimeField(auto_now_add=True, auto_now=True, blank=True, null=True)
    last_modified_by = models.ForeignKey(Member, related_name='%(class)s_last_modified')

    #aggrgated
    total_votes = models.PositiveIntegerField(default=0)
    total_favourites = models.PositiveIntegerField(default=0, editable=False)

    class Meta:
        abstract = True
        app_label = 'core'