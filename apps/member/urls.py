from django.urls import include, re_path

from .views import MemberProfileView
from .views import Signup
from .views import MemberRequestResetPasswordView
from .views import MemberRequestResetPasswordDone
from .views import login
from .views import logout
from .views import change_password
from .views import update_profile
from .views import activate
from .views import reset_password


urlpatterns = [
    re_path(r"signup$", Signup.as_view(), name="signup"),
    re_path(r"login$", login, name="login"),
    re_path(r"logout$", logout, name="logout"),
    re_path(r"change_password$", change_password, name="change_password"),
    re_path(r"update_profile$", update_profile, name="update_profile"),
    re_path(r"activate/(?P<activation_key>\w+)/$", activate, name="activate_account"),
    re_path(r"(?P<pk>\d+)/$", MemberProfileView.as_view(), name="member_profile"),
    re_path(
        r"request_reset_password$",
        MemberRequestResetPasswordView.as_view(),
        name="member_request_reset_pwd",
    ),
    re_path(
        r"request_reset_password_done$",
        MemberRequestResetPasswordDone.as_view(),
        name="member_request_reset_pwd_done",
    ),
    re_path(
        r"reset_password/(?P<user_id>\d+)/(?P<pwd_reset_token>\w+)/$",
        reset_password,
        name="reset_password",
    ),
]
