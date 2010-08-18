from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('twitter.views',
    url(r'^$', 'index', name='tweets'),
)