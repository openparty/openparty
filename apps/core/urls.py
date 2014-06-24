from feeds import Events_Feed, Topics_Feed, Posts_Feed
from django.views.generic import TemplateView
from django.conf.urls import patterns, url

event_patterns = patterns('apps.core.views',
    url(r'^$', 'event_list', name='event_list'),
    url(r'^join/?$', 'join_event'),
    url(r'^checkin$', 'checkin', name='event_checkin'),
    url(r'^(?P<id>\d+)$', 'event', name='event'),
)

topic_patterns = patterns('apps.core.views',
    url(r'^$', 'topic_list', name='topic_list'),
    url(r'^(?P<id>\d+)$', 'topic', name='topic'),
    url(r'^new/?$', 'submit_topic', name='submit_new_topic'),
    url(r'^(?P<id>\d+)/edit/?$', 'edit_topic', name='edit_topic'),
    url(r'^(?P<id>\d+)/vote$', 'vote'),
    url(r'^(?P<id>\d+)/votes$', 'votes_for_topic', name='vote_for_topic'),
)

feed_patterns = patterns('apps.core.views',
    url(r'^event/?$', Events_Feed(), name="feed_events"),
    url(r'^topic/?$', Topics_Feed(), name="feed_topics"),
    url(r'^post/?$', Posts_Feed(), name="feed_posts"),
)

post_patterns = patterns('apps.core.views',
    url(r'^$', 'list_post', name='list_post'),
    url(r'^(?P<id>\d+)/?$', 'view_post', name='view_post'),
    url(r'^(?P<name>[^/]*)/?$', 'view_post_by_name', name='view_post_by_name'),
)

wordpress_redirect_patterns = patterns('apps.core.views',
    url(r'^(?P<name>[^/]*)/?$', 'redirect_wordpress_post', name='redirect_wordpress_post'),
)

about_patterns = patterns('django.views.generic',
    url(r'^/?$', TemplateView.as_view(template_name='core/about.html'), name="about"),
)
