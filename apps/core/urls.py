from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('core.views',
    url(r'^checkin$', 'checkin', name='event_checkin'),
)