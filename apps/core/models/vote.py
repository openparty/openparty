# -*- coding: utf-8 -*-
from django.db import models

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from apps.member.models import Member


class Vote(models.Model):
    """A Vote for Topic, Event or Comment"""

    user = models.ForeignKey(
        Member,
        related_name="vote_created",
        verbose_name=u"用户",
        on_delete=models.SET_NULL,
        null=True,
    )
    rating = models.FloatField("评分", default=0)

    content_type = models.ForeignKey(
        ContentType,
        limit_choices_to={"model__in": ("topic", "event", "comment")},
        on_delete=models.PROTECT,
    )
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey("content_type", "object_id")
    created = models.DateTimeField("创建日期", auto_now_add=True)
    # denorm
    item_raw = models.TextField("item raw", blank=True)
    user_raw = models.TextField("user raw", blank=True)

    class Meta:
        app_label = "core"

    def __unicode__(self):
        return u"%s 投票给 %s" % (self.user, self.item)
