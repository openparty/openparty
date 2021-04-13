from django.views.generic import TemplateView
from django.conf.urls import url
from .feeds import Events_Feed, Topics_Feed, Posts_Feed
from apps.core.views import EventList, TopicList
from django.urls import include, re_path
from .views import join_event
from .views import checkin
from .views import event
from .views import topic
from .views import submit_topic
from .views import edit_topic
from .views import vote
from .views import votes_for_topic
from .views import list_post
from .views import view_post
from .views import view_post_by_name
from .views import redirect_wordpress_post


event_patterns = [
    re_path(r'^$', EventList.as_view(), name='event_list'),
    re_path(r'^join/?$', join_event),
    re_path(r'^checkin$', checkin, name='event_checkin'),
    re_path(r'^(?P<id>\d+)$', event, name='event'),
]

topic_patterns = [
    re_path(r'^$', TopicList.as_view(), name='topic_list'),
    re_path(r'^(?P<id>\d+)$', topic, name='topic'),
    re_path(r'^new/?$', submit_topic, name='submit_new_topic'),
    re_path(r'^(?P<id>\d+)/edit/?$', edit_topic, name='edit_topic'),
    re_path(r'^(?P<id>\d+)/vote$', vote),
    re_path(r'^(?P<id>\d+)/votes$', votes_for_topic, name='vote_for_topic'),
]

feed_patterns = [
    re_path(r'^event/?$', Events_Feed(), name="feed_events"),
    re_path(r'^topic/?$', Topics_Feed(), name="feed_topics"),
    re_path(r'^post/?$', Posts_Feed(), name="feed_posts"),
]

post_patterns = [
    re_path(r'^$', list_post, name='list_post'),
    re_path(r'^(?P<id>\d+)/?$', view_post, name='view_post'),
    re_path(r'^(?P<name>[^/]*)/?$', view_post_by_name, name='view_post_by_name'),
]

wordpress_redirect_patterns = [
    re_path(r'^(?P<name>[^/]*)/?$', redirect_wordpress_post, name='redirect_wordpress_post'),
]

about_patterns = [
    re_path(r'^$', TemplateView.as_view(template_name='core/about.html'), name="about"),
]
