# -*- encoding: utf-8 -*-
from django.urls import reverse
from django.contrib.syndication.views import Feed


import settings


class Events_Feed(Feed):

    title = "Beijing OpenParty 最新活动列表"
    link = settings.SITE_URL + "/event"
    author_link = link
    description = "发布 Beijing OpenParty 的最新活动信息"

    def root_attributes(self):
        attrs = super(Events_Feed, self).root_attributes()
        attrs["atom:links"] = "http://www.itunes.com/dtds/podcast-1.0.dtd"
        return attrs

    def items(self):
        from apps.core.models.event import Event
        return Event.objects.order_by("-begin_time")

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.description

    def item_link(self, item):
        return settings.SITE_URL + item.get_absolute_url()


class Topics_Feed(Feed):

    title = "Beijing OpenParty 最新话题列表"
    link = settings.SITE_URL + "/topic"
    description = "发布 Beijing OpenParty 的最新活动中的话题信息"

    def items(self):
        from apps.core.models.topic import Topic
        return Topic.objects.all().order_by(
            "-in_event__begin_time", "-accepted", "-total_votes"
        )

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.description

    def item_link(self, item):
        return settings.SITE_URL + item.get_absolute_url()


class Posts_Feed(Feed):

    title = "Beijing OpenParty 最新新闻"
    link = settings.SITE_URL + "/post"
    description = "Beijing OpenParty 最新新闻"

    def items(self):
        from apps.core.models.post import Post
        return Post.objects.all().order_by("-created_at")

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content

    def item_link(self, item):
        return settings.SITE_URL + item.get_absolute_url()
