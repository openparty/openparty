from django.conf.urls.defaults import patterns, include, url, handler500, handler404
from settings import MEDIA_ROOT
from django.contrib import admin

from apps.core.urls import event_patterns, topic_patterns, feed_patterns, post_patterns, about_patterns


admin.autodiscover()
urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^member/', include('member.urls')),
    (r'^event/', include(event_patterns)),
    (r'^topic/', include(topic_patterns)),
    (r'^feed/', include(feed_patterns)),
    (r'^post/', include(post_patterns)),
    (r'^tweets', include('twitter.urls')),
    (r'^about/', include(about_patterns)),
)

urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^xmlrpc/$', 'django_xmlrpc.views.handle_xmlrpc', {}, 'xmlrpc'),  #for pingback handle
)

urlpatterns += patterns('apps.core.views',
    url(r'^index$', 'index', name='index'),
    url(r'^/?$', 'index'),
)
