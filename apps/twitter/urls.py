from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('twitter.views',
    url(r'^$', 'index', name='tweets'),
    url(r'^/request_oauth$', 'request_oauth', name='request_oauth'),
    url(r'^/oauth_callback$', 'oauth_callback', name='oauth_callback'),
    url(r'^/update$', 'update', name='update_tweet'),
    url(r'^/delete$', 'delete', name='delete_tweet'),
)
