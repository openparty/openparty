from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('member.views',
    url(r'^signup$', 'signup', name='signup'),
    url(r'^login$', 'login', name='login'),
    url(r'^logout$', 'logout', name='logout'),
    url(r'^change_password$', 'change_password', name='change_password'),
    url(r'^update_profile$', 'update_profile', name='update_profile'),
    url(r'^activate/(?P<activation_key>\w+)/$', 'activate', name='activate_account'),
)