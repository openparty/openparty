from feeds import Events_Feed, Topics_Feed
from django.conf.urls.defaults import patterns, url

event_patterns = patterns('core.views',
    url(r'^$', 'event_list', name='event_list'),
    url(r'^join$', 'join_event'),
    url(r'^checkin$', 'checkin', name='event_checkin'),
    url(r'^(?P<id>\d+)$', 'event', name='event'),
)

topic_patterns = patterns('core.views',
    url(r'^$', 'topic_list', name='topic_list'),
    url(r'^(?P<id>\d+)$', 'topic', name='topic'),
    url(r'^new/?$', 'submit_topic', name='submit_new_topic'),
    url(r'^(?P<id>\d+)/edit/?$', 'edit_topic', name='edit_topic'),
    url(r'^(?P<id>\d+)/vote$', 'vote'),
    url(r'^(?P<id>\d+)/votes$', 'votes_for_topic', name='vote_for_topic'),
)

feed_patterns = patterns('core.views',
    url(r'^event/?$', Events_Feed(), name="feed_events"),
    url(r'^topic/?$', Topics_Feed(), name="feed_topics"),
)

post_patterns = patterns('core.views',
    url(r'^$', 'list_post', name='list_post'),
)
