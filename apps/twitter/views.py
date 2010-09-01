# -*- coding: utf-8 -*-
# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib import messages
import tweepy
from settings import TWITTER_OPENPARTY_KEY, TWITTER_OPENPARTY_SECRET

from apps.twitter.models import Tweet
from apps.member.models import Member


def index(request):
    tweets = Tweet.objects.order_by('-tweet_id')[:100]
    ctx = {'tweets': tweets,
           'tab': 'tweet',
          }
    return render_to_response('twitter/index.html', ctx, context_instance=RequestContext(request))

@login_required
def request_oauth(request):
    member = Member.objects.get(user=request.user)
    auth = tweepy.OAuthHandler(TWITTER_OPENPARTY_KEY, TWITTER_OPENPARTY_SECRET)
    try:
        redirect_url = auth.get_authorization_url()
    except tweepy.TweepError:
        render_to_response('500.html', {'error_message': u'无法从twitter.com获取redirect url'}, context_instance=RequestContext(request))

    member.twitter_access_token_key = auth.request_token.key
    member.twitter_access_token_secret = auth.request_token.secret
    if member.twitter_enabled:
        member.twitter_enabled = False
    member.save()

    return redirect(redirect_url, permanent=False)

@login_required
def oauth_callback(request):
    member = Member.objects.get(user=request.user)
    member.twitter_enabled = True
    member.save()

    messages.info(request, u'恭喜，您已经成功通过了Twitter的OAuth认证！以后您就可以在这里发推了。')
    return redirect(reverse('tweets'))
