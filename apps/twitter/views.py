# -*- coding: utf-8 -*-
# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib import messages
import tweepy
from settings import TWITTER_OPENPARTY_KEY, TWITTER_OPENPARTY_SECRET

import hashlib

from apps.twitter.models import Tweet
from apps.member.models import Member


def index(request):
    twitter_enabled = False
    if hasattr(request, 'user'):
        
        admin_mail_sha1_hash = ('c4a1f1d86ccd8981e9ea8cb3027c848d362bacd4', #cnborn
                           '72056e7da242b31ca6638fd208560620062212a9', #tin
                           'f26995abecc6e1edf01e1b9a5e3dc6c0317a49ea', #makestory
                           '0ed17b80ebae26e1b28d9caef21c5425d49f78cb', #conglin
                           '6356945b9581d8049c73ea6e94760c8b2c6303cb', #cleverpig
                           )

        if hashlib.sha1(request.user.username.lower()).hexdigest() in admin_mail_sha1_hash:
            twitter_enabled = True
    tweets = Tweet.objects.order_by('-tweet_id')[:100]
    paginator = Paginator(tweets, 50)

    try:
        page_num = int(request.GET.get('page', '1'))
    except ValueError:
        page_num = 1
    
    try:
        page = paginator.page(page_num)
    except (EmptyPage, InvalidPage):
        page = paginator.page(paginator.num_pages)

    ctx = {
        'page': page,
        'tweets': page.object_list,
        'tab': 'tweet',
        'twitter_enabled': twitter_enabled
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
    auth = tweepy.OAuthHandler(TWITTER_OPENPARTY_KEY, TWITTER_OPENPARTY_SECRET)
    try:
        auth.set_request_token(member.twitter_access_token_key, member.twitter_access_token_secret)
        auth.get_access_token()
        member.twitter_access_token_key = auth.access_token.key
        member.twitter_access_token_secret = auth.access_token.secret
        member.twitter_enabled = True
        member.save()
        messages.info(request, u'恭喜，您已经成功通过了Twitter的OAuth认证！以后您就可以在这里发推了。')
    except tweepy.TweepError:
        messages.error(request, u'对不起，认证的过程中发生了错误')

    return redirect(reverse('tweets'))

@login_required
def update(request):
    member = Member.objects.get(user=request.user)
    status = request.POST.get('status')
    if member.twitter_enabled:
        auth = tweepy.OAuthHandler(TWITTER_OPENPARTY_KEY, TWITTER_OPENPARTY_SECRET)
        auth.set_access_token(member.twitter_access_token_key, member.twitter_access_token_secret)
        api = tweepy.API(auth)
        api.update_status(status)
        messages.info(request, u'Sent!')
    else:
        messages.error(request, u'对不起您还没有通过Twitter的OAuth认证')
    return redirect(reverse('tweets'))
