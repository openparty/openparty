from django.conf.urls.defaults import patterns, include, url
from openparty.settings import MEDIA_ROOT

from django.conf.urls.defaults import handler404, handler500
#not adding above line may cause a 'handler404, 500 not found' problem in testcase.
#http://code.djangoproject.com/ticket/11013#comment:1

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^openparty/', include('openparty.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    # Media path
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}),
    (r'^comments/', include('django.contrib.comments.urls')),
)

urlpatterns += patterns('openparty.apps.core.views',
    (r'^index$', 'index'),
    (r'^/?$', 'index'),
    (r'^events$', 'event_list'),
    (r'^topics$', 'topic_list'),
    (r'^event/join$', 'join_event'),
    (r'^event/(?P<id>\d+)$', 'event'),
    (r'^topic/(?P<id>\d+)$', 'topic'),
    (r'^vote/topic/(?P<id>\d+)$', 'vote'),
    url(r'^topic/submit/?$', 'submit_topic', name='submit_new_topic'),
    url(r'^topic/edit/(?P<id>\d+)/?$', 'edit_topic', name='edit_topic'),
)

urlpatterns += patterns('openparty.apps.member.views',
    (r'^signup$', 'signup'),
    (r'^login$', 'login'),
    (r'^logout$', 'logout'),
    (r'^change_password$', 'change_password'),
    (r'^update_profile$', 'update_profile'),
    (r'^activate/(?P<activation_key>\w+)/$', 'activate'),
)
