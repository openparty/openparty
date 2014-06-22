from django.conf.urls import patterns, include, url, handler404
from django.contrib import admin

from apps.core.urls import event_patterns, topic_patterns, feed_patterns, post_patterns, about_patterns, wordpress_redirect_patterns


admin.autodiscover()
urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^member/', include('apps.member.urls')),
    (r'^event/', include(event_patterns)),
    (r'^topic/', include(topic_patterns)),
    (r'^feed/', include(feed_patterns)),
    (r'^post/', include(post_patterns)),
    (r'^tweets', include('apps.twitter.urls')),
    (r'^about/', include(about_patterns)),
    (r'^(?P<year>\d{4})/(?P<month>\d{1,2})/', include(wordpress_redirect_patterns)),
)

urlpatterns += patterns('',
    #(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': STATIC_ROOT}),
    (r'^comments/', include('django.contrib.comments.urls')),
)

urlpatterns += patterns('apps.core.views',
    url(r'^index$', 'index', name='index'),
    url(r'^/?$', 'index'),
)

def handler500(request):
    """
    An error handler which exposes the request object to the error template.
    """
    from django.template import Context, loader
    from django.http import HttpResponseServerError
    from raven.contrib.django.models import sentry_exception_handler

    import logging
    import sys

    sentry_exception_handler(request=request)
    context = { 'request': request }

    t = loader.get_template('500.html') # You need to create a 500.html template.
    return HttpResponseServerError(t.render(Context(context)))
