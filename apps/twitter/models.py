# -*- coding: utf-8 -*-
try:
    import json
except:
    from django.utils import simplejson as json

import tweepy

import time
from lxml import html
from datetime import datetime
from django.db import models
import urllib, urllib2
from cookielib import CookieJar

class TweetManager(models.Manager):

    def search(self, query='#openparty', limit=5, since=None, page=1):
        tweets = tweepy.api.search(q=query, rpp=limit, since_id=since, page=page)
        return [self.model.create_from_tweepy_tweet(tweet=tweet) for tweet in tweets]
    
    def sync(self, query='#openparty', since=None):
        if since:
            max_tweet_id = since # for test only
        else:
            max_tweet_id = self.filter(query=query).aggregate(models.Max('tweet_id'))['tweet_id__max']
        print 'Syncing new tweets of %s (newer than %s)' % (query, max_tweet_id)
        new_tweets = self.search(query=query, limit=100, since=max_tweet_id, page=1)
        if len(new_tweets):
            for tweet in new_tweets:
                tweet.query = query
                tweet.save()
            return len(new_tweets)
        else:
            return 0
    
    def sync_all(self, query='#openparty'):
        page = 1
        count = 0
        print 'Syncing all of %s' % query
        while True:
            tweets = tweepy.api.search(q=query, rpp=50, page=page)
            page += 1
            if len(tweets) == 0:
                break
            for tweet in tweets:
                t = self.model.create_from_tweepy_tweet(tweet=tweet)
                t.query = query
                t.save()
                count += 1
            print 'synced %s tweets' % count
            time.sleep(5)
        return count
    
    def sync_weibo(self, query='#openparty'):
        weibo_query = urllib.quote(urllib.quote(query))
        username = 'iamtin%40gmail.com'
        password = '111111'

        def add_headers(req):
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7')
            req.add_header('Referer', 'http://t.sina.com.cn/')
            return req

        post_data = 'client=ssologin.js(v1.3.9)&encoding=utf-8&' +\
                    'entry=miniblog&from=&gateway=1&password=' + password +\
                    '&returntype=META&savestate=7&service=miniblog&' +\
                     'url=http%3A%2F%2Ft.sina.com.cn%2Fajaxlogin.php%3Fframelogin%3D1%26c' +\
                     'allback%3Dparent.sinaSSOController.feedBackUrlCallBack&' +\
                     'username=' + username + '&useticket=0'

        post_url = 'http://login.sina.com.cn/sso/login.php'
        
        cookie = CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
        urllib2.install_opener(opener)

        # login
        req = urllib2.Request(url=post_url, data=post_data)
        req = add_headers(req)
        response = urllib2.urlopen(req)
        
        # do the real search
        search_req = urllib2.Request(url='http://t.sina.com.cn/k/%2523openparty')
        req = add_headers(search_req)
        response = urllib2.urlopen(search_req)
        htm = response.read()
        page = html.fromstring(htm)
        tweets_list = page.cssselect('#feed_list li')
        tweets = []
        for tweet_element in tweets_list:
            tweet = self.model.create_from_weibo_html_fragment(tweet_element)
            if not tweet.is_duplicated():
                tweet.save()
                tweets.append(tweet)
        return len(tweets)

# Create your models here.
class Tweet(models.Model):
    """(A model represent the tweets of twitter.com)"""
    tweet_id = models.BigIntegerField(blank=False, null=False, unique=True)
    profile_image = models.CharField(blank=True, null=True, max_length=255)
    text = models.TextField(blank=True, null=False, max_length=512)
    language = models.CharField(blank=True, null=True, max_length=16)
    geo = models.CharField(blank=True, null=True, max_length=80)
    tweet_user_id = models.BigIntegerField(blank=True, null=False)
    tweet_user_name = models.CharField(blank=True, null=True, max_length=128)
    craeted_at = models.DateTimeField(blank=True, null=True)
    source = models.CharField(blank=True, null=True, max_length=80)
    dump = models.TextField(blank=True, null=False)
    query = models.CharField(blank=True, null=True, max_length=127)
    race = models.CharField(blank=True, null=True, max_length=16)
    uri = models.CharField(blank=True, null=True, max_length=512)
    
    objects = TweetManager()
    
    class Meta:
        ordering = []
        verbose_name, verbose_name_plural = "Tweet", "s"

    def __unicode__(self):
        return u"Tweet"
    
    def is_duplicated(self):
        try:
            self.__class__.objects.get(tweet_id=self.tweet_id)
            return True
        except self.DoesNotExist:
            return False
    
    @classmethod
    def create_from_tweepy_tweet(cls, tweet):
        my_tweet = cls()
        my_tweet.race = 'twitter'
        my_tweet.tweet_id = tweet.id
        my_tweet.profile_image = tweet.profile_image_url
        my_tweet.text = tweet.text
        my_tweet.language = tweet.iso_language_code
        my_tweet.geo = tweet.geo
        my_tweet.tweet_user_id = tweet.from_user_id
        my_tweet.tweet_user_name = tweet.from_user
        my_tweet.created_at = tweet.created_at
        my_tweet.source = tweet.source
        d = tweet.__dict__.copy()
        d.pop('created_at')
        my_tweet.dump = json.dumps(d)
        return my_tweet
    
    @classmethod
    def create_from_weibo_html_fragment(cls, ele):
        t = cls()
        t.dump = html.tostring(ele)
        t.race = 'weibo'
        # tweet_id
        smss = ele.cssselect('.MIB_feed_c .sms')
        if len(smss) == 1:
            t.tweet_id = int(smss[0].get('mid'))
        # profile_image, user_id, user_name
        images = ele.cssselect('.head_pic img')
        if len(images) == 1:
            user_image = images[0]
            t.profile_image = user_image.get('src')
            t.tweet_user_id = int(user_image.get('uid'))
            t.tweet_user_name = user_image.get('title')
        # created_at
        created_ats = ele.cssselect('.feed_att cite strong')
        if len(created_ats) == 1:
            created_at = created_ats[0]
            time_str = created_at.text_content()
            if time_str.find(u'月') != -1:
                this_year = datetime.today().year
                time_str = u'%s年%s' % (this_year, time_str)
                t.created_at = datetime.strptime(time_str.encode('utf-8'), '%Y年%m月%d日 %H:%M')
            else:
                t.created_at = datetime.strptime(time_str, '%Y-%m-%d %H:%M')
        # uri
        uris = ele.cssselect(".feed_att a[href^='http://t.sina.com.cn']")
        if len(uris) == 1:
            t.uri = uris[0].get('href')
        # source
        attr = ele.cssselect('.feed_att .lf')
        if len(attr) == 1:
            attr_text = attr[0].text_content()
            idx = attr_text.find(u'来自')
            if idx != -1:
                t.source = attr_text[idx+2:].strip()
        # text
        contents = ele.cssselect('.MIB_feed_c')
        if len(contents) == 1:
            t.text = html.tostring(contents[0])
        return t

    @models.permalink
    def get_absolute_url(self):
        return ('Tweet', [self.id])
