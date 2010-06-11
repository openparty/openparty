from django.conf.urls.defaults import patterns, include, url, handler500, handler404
from settings import MEDIA_ROOT
from django.contrib import admin
import member

admin.autodiscover()
urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^member/', include('member.urls')),
)

urlpatterns += patterns('',
    # Media path
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}),
    (r'^comments/', include('django.contrib.comments.urls')),
)


urlpatterns += patterns('apps.core.views',
    (r'^index$', 'index'),
    (r'^/?$', 'index'),
    (r'^events$', 'event_list'),
    (r'^topics$', 'topic_list'),
    (r'^event/join$', 'join_event'),
    url(r'^event/(?P<id>\d+)$', 'event', name='event'),
    (r'^topic/(?P<id>\d+)/votes$', 'votes_for_topic'),
    url(r'^topic/(?P<id>\d+)$', 'topic', name='topic'),
    (r'^vote/topic/(?P<id>\d+)$', 'vote'),
    url(r'^topic/submit/?$', 'submit_topic', name='submit_new_topic'),
    url(r'^topic/edit/(?P<id>\d+)/?$', 'edit_topic', name='edit_topic'),
)

urlpatterns += patterns('apps.twitter.views',
    (r'^tweets$', 'index'),
)
