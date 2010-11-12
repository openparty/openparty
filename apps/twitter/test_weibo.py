#!/usr/bin/env python
# encoding: utf-8
from django.test import TestCase
from django.db import models
from django.core.urlresolvers import reverse
from apps.twitter.models import Tweet
from lxml import html
from datetime import datetime, timedelta


weibo_sms_html_frag = u'''
<li id="mid_211101110530573" class="MIB_linedot2">
  <div class="head_pic"><a href="http://t.sina.com.cn/lanyueniao"><img src="http://tp3.sinaimg.cn/1661931502/50/1287680537/1" imgtype="head" uid="1661931502" title="蓝月鸟"></a>
</div>
  <div class="MIB_feed_c">
    <p type="3" mid="211101110530573" class="sms"><a title="蓝月鸟" href="http://t.sina.com.cn/lanyueniao">蓝月鸟</a>：我们是海盗！</p>
    <div class="MIB_assign">
  <div class="MIB_asarrow_l"></div>
  <div class="MIB_assign_t"></div>
  <div class="MIB_assign_c MIB_txtbl"> 
    <p type="2" mid="211101110530573" class="source">
      <a href="http://t.sina.com.cn/1646023983">@cleverpig</a>：继续邀请一位航海家到<a href="http://t.sina.com.cn/k/openparty">#openparty#</a>分享话题，半年前已经邀请过但不巧没有成行，继续努力！祈求上帝保佑～
    <span class="source_att MIB_linkbl"><a href="http://t.sina.com.cn/1646023983/24EN12cPh"><strong lang="CL1005">原文转发</strong><strong type="rttCount" rid="211101110525963">(2)</strong></a><span class="MIB_line_l">|</span><a href="http://t.sina.com.cn/1646023983/24EN12cPh"><strong lang="CC0603">原文评论</strong><strong type="commtCount" rid="211101110525963">(5)</strong></a></span></p>
    <div id="prev_211101110530573" class="feed_preview">
            <div class="clear"></div>
    </div>
    <div style="display:none;" id="disp_211101110530573" class="blogPicOri"> </div>
     </div>
  <div class="MIB_assign_b"></div>
</div>
        <div class="feed_att">
      <div class="lf MIB_txtbl"><cite><a href="http://t.sina.com.cn/1661931502/24EN12e1D"><strong>11月10日 11:19</strong></a></cite>
<strong lang="CL1006">来自</strong><cite><a target="_blank" href="https://chrome.google.com/extensions/detail/aicelmgbddfgmpieedjiggifabdpcnln?hl=zh-cn">FaWave</a></cite></div>
      <div class="rt"><a onclick="App.ModForward('211101110530573','%E7%BB%A7%E7%BB%AD%E9%82%80%E8%AF%B7%E4%B8%80%E4%BD%8D%E8%88%AA%E6%B5%B7%E5%AE%B6%E5%88%B0%3Ca%20href%3D%22http%3A%2F%2Ft.sina.com.cn%2Fk%2Fopenparty%22%3E%23openparty%23%3C%2Fa%3E%E5%88%86%E4%BA%AB%E8%AF%9D%E9%A2%98%EF%BC%8C%E5%8D%8A%E5%B9%B4%E5%89%8D%E5%B7%B2%E7%BB%8F%E9%82%80%E8%AF%B7%E8%BF%87%E4%BD%86%E4%B8%8D%E5%B7%A7%E6%B2%A1%E6%9C%89%E6%88%90%E8%A1%8C%EF%BC%8C%E7%BB%A7%E7%BB%AD%E5%8A%AA%E5%8A%9B%EF%BC%81%E7%A5%88%E6%B1%82%E4%B8%8A%E5%B8%9D%E4%BF%9D%E4%BD%91%EF%BD%9E',0,this,'num_211101110530573','蓝月鸟','%E6%88%91%E4%BB%AC%E6%98%AF%E6%B5%B7%E7%9B%97%EF%BC%81','')" initblogername="cleverpig" initbloger="1646023983" lastforwardername="蓝月鸟" lastforwarder="1661931502" href="javascript:void(0);"><strong lang="CD0023">转发</strong><strong type="rttCount" rid="211101110530573" id="num_211101110530573"></strong></a>
<span class="navBorder">|</span>
<a onclick="App.addfavorite_miniblog('211101110530573');" href="javascript:void(0);"><strong lang="CL1003">收藏</strong></a>
<span class="navBorder">|</span>
<a onclick="scope.loadCommentByRid(1661931502, 'miniblog2', '新浪微博', '211101110530573', '%E6%88%91%E4%BB%AC%E6%98%AF%E6%B5%B7%E7%9B%97%EF%BC%81', '', '', 1, 0, 1);" href="javascript:void(0);" id="_comment_count_miniblog2_211101110530573"><strong lang="CL1004">评论</strong><strong type="commtCount" rid="211101110530573"></strong></a>
</div>
    </div>
    <div id="_comment_list_miniblog2_211101110530573"></div>
  </div>
</li>
'''

class WeiboTest(TestCase):
    # def test_login_to_weibo(self):
    #         post_data = 'client=ssologin.js(v1.3.9)&encoding=utf-8&' +\
    #             'entry=miniblog&from=&gateway=1&password=' + self.password +\
    #             '&returntype=META&savestate=7&service=miniblog&' +\
    #              'url=http%3A%2F%2Ft.sina.com.cn%2Fajaxlogin.php%3Fframelogin%3D1%26c' +\
    #              'allback%3Dparent.sinaSSOController.feedBackUrlCallBack&' +\
    #              'username=' + self.username + '&useticket=0'
    # 
    #         post_url = 'http://login.sina.com.cn/sso/login.php'
    #         
    #         cookie = CookieJar()
    #         opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    #         urllib2.install_opener(opener)
    # 
    #         req = urllib2.Request(url=post_url, data=post_data)
    #         req = self._add_headers(req)
    #         response = urllib2.urlopen(req)
    #         # print dir(response)
    #         
    #         search_req = urllib2.Request(url='http://t.sina.com.cn/k/%2523openparty')
    #         req = self._add_headers(search_req)
    #         response = urllib2.urlopen(search_req)
    #         print response.info()
    #         print response.headers
    #         print response.read()
    #     
    #     def _add_headers(self, req):
    #         req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7')
    #         req.add_header('Referer', 'http://t.sina.com.cn/')
    #         return req
    
    def test_tweet_should_have_id_when_create_it_from_weibo_html_fragment(self):
        ele = html.fromstring(weibo_sms_html_frag)
        t = Tweet.create_from_weibo_html_fragment(ele)
        self.assertEquals(211101110530573L, t.tweet_id)
    
    def test_tweet_should_have_profile_image_when_create_it_from_weibo_html_fragment(self):
        ele = html.fromstring(weibo_sms_html_frag)
        t = Tweet.create_from_weibo_html_fragment(ele)
        self.assertEquals('http://tp3.sinaimg.cn/1661931502/50/1287680537/1', t.profile_image)
    
    def test_tweet_should_have_user_id_when_create_it_from_weibo_html_fragment(self):
        ele = html.fromstring(weibo_sms_html_frag)
        t = Tweet.create_from_weibo_html_fragment(ele)
        self.assertEquals(u'蓝月鸟', t.tweet_user_name)
        self.assertEquals(1661931502L, t.tweet_user_id)
    
    def test_tweet_should_have_created_at_time_when_create_it_from_weibo_html_fragment(self):
        ele = html.fromstring(weibo_sms_html_frag)
        t = Tweet.create_from_weibo_html_fragment(ele)
        created_at = datetime(2010, 11, 10, 11, 19)
        self.assertEquals(created_at.strftime('%Y%m%d %H%M%S'), t.created_at.strftime('%Y%m%d %H%M%S'))

        m = weibo_sms_html_frag.replace(u'11月10日 11:19', '2009-8-29 16:55')
        ele = html.fromstring(m)
        t = Tweet.create_from_weibo_html_fragment(ele)
        created_at = datetime(2009, 8, 29, 16, 55)
        self.assertEquals(created_at.strftime('%Y%m%d %H%M%S'), t.created_at.strftime('%Y%m%d %H%M%S'))
        
        m = weibo_sms_html_frag.replace(u'11月10日 11:19', u'18分钟前')
        ele = html.fromstring(m)
        t = Tweet.create_from_weibo_html_fragment(ele)
        created_at = datetime.now() - timedelta(seconds=60*18)
        self.assertEquals(created_at.strftime('%Y%m%d %H%M%S'), t.created_at.strftime('%Y%m%d %H%M%S'))
    
    def test_tweet_should_have_source_when_create_it_from_weibo_html_fragment(self):
        ele = html.fromstring(weibo_sms_html_frag)
        t = Tweet.create_from_weibo_html_fragment(ele)
        self.assertEquals('FaWave', t.source)
    
    def test_tweet_should_have_dump_which_is_the_original_html_fragment(self):
        ele = html.fromstring(weibo_sms_html_frag)
        t = Tweet.create_from_weibo_html_fragment(ele)
        self.assertEquals(html.tostring(ele), t.dump)
    
    def test_weibo_tweet_should_be_weibo_race(self):
        ele = html.fromstring(weibo_sms_html_frag)
        t = Tweet.create_from_weibo_html_fragment(ele)
        self.assertEquals('weibo', t.race)
    
    def test_weibo_tweet_should_have_uri(self):
        ele = html.fromstring(weibo_sms_html_frag)
        t = Tweet.create_from_weibo_html_fragment(ele)
        self.assertEquals('http://t.sina.com.cn/1661931502/24EN12e1D', t.uri)
    
    def test_weibo_tweet_should_use_original_content_as_text(self):
        ele = html.fromstring(weibo_sms_html_frag)
        t = Tweet.create_from_weibo_html_fragment(ele)
        ele = html.fromstring(t.text)
        self.assertEquals('MIB_feed_c', ele.get('class'))

__test__ = {}