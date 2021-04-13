from django.conf.urls import include, url, handler404
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.urls import include, re_path

from apps.core.urls import event_patterns, topic_patterns, feed_patterns, post_patterns, about_patterns, wordpress_redirect_patterns
from apps.core.views import index


admin.autodiscover()
urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^member/', include('apps.member.urls')),
    re_path(r'^event/', include(event_patterns)),
    re_path(r'^topic/', include(topic_patterns)),
    re_path(r'^feed/', include(feed_patterns)),
    re_path(r'^post/', include(post_patterns)),
    re_path(r'^tweets/', include('apps.twitter.urls')),
    re_path(r'^about', include(about_patterns)),
    re_path(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/', include(wordpress_redirect_patterns)),
]

urlpatterns += [
    #(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': STATIC_ROOT}),
    url(r'^comments/', include('django_comments.urls')),
]

urlpatterns += [
    re_path(r'^index$', index, name='index'),
    re_path(r'^$', index),
]

urlpatterns += staticfiles_urlpatterns()

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
