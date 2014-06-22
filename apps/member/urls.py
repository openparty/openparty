from django.conf.urls import patterns, url
from apps.member.views import MemberProfileView
from apps.member.views import MemberRequestResetPasswordView, MemberRequestResetPasswordDone

urlpatterns = patterns('apps.member.views',
    url(r'^signup$', 'signup', name='signup'),
    url(r'^login$', 'login', name='login'),
    url(r'^logout$', 'logout', name='logout'),
    url(r'^change_password$', 'change_password', name='change_password'),
    url(r'^update_profile$', 'update_profile', name='update_profile'),
    url(r'^activate/(?P<activation_key>\w+)/$', 'activate', name='activate_account'),
    url(r'^(?P<pk>\d+)/$', MemberProfileView.as_view(), name='member_profile'),
    url(r'^request_reset_password$', MemberRequestResetPasswordView.as_view(), name='member_request_reset_pwd'),
    url(r'^request_reset_password_done$', MemberRequestResetPasswordDone.as_view(), name='member_request_reset_pwd_done'),
    url('^reset_password/(?P<user_id>\d+)/(?P<pwd_reset_token>\w+)/$', 'reset_password', name='reset_password'),
)
