from django.urls import include, re_path

from .models import Tweet
from .views import index
from .views import request_oauth
from .views import oauth_callback
from .views import update
from .views import delete

urlpatterns = [
    re_path(r"^$", index, name="tweets"),
    re_path(r"^request_oauth$", request_oauth, name="request_oauth"),
    re_path(r"^oauth_callback$", oauth_callback, name="oauth_callback"),
    re_path(r"^update$", update, name="update_tweet"),
    re_path(r"^delete$", delete, name="delete_tweet"),
]
