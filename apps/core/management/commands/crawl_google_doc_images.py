#!/usr/bin/env python
# encoding: utf-8
import sys
from django.conf import settings
from django.core.management.base import BaseCommand
from lxml import html
from lxml.cssselect import CSSSelector
from hashlib import md5
import urllib2
import traceback
import os

from apps.core.models import Post

class Command(BaseCommand):

    url_image_mapping_file = 'url_image_mapping_file.out'
    image_folder = 'crawl_iamges'
    m = md5()
    mapping = {}

    def handle(self, *args, **options):
        if len(args) == 0:
            self._usage()
            return
        
        if 'down' == args[0]:
            self.download()
        elif 'replace' == args[0]:
            self.replace()
        else:
            self._usage()
            
    def _usage(self):
        print 'Usage: ./manage.py crawl_google_doc_images [down|replace]'
    
    def replace(self):
        with open(self.url_image_mapping_file) as f:
            for line in f:
                line = line.strip()
                if not line.startswith('Failed'):
                    url, filename = line.split('->')
                    self.mapping[url.strip()] = filename.strip()

        posts = Post.objects.all()

        for post in posts:
            page_element = html.fromstring(post.content)
            image_selector = CSSSelector('img')
            images = image_selector(page_element)
            for image in images:
                url = image.attrib['src'].strip()
                if url in self.mapping:
                    image.attrib['src'] = "/post_images/%s" % self.mapping[url]
                    print 'replace %s with %s' % (url, self.mapping[url])
            post.content = html.tostring(page_element)
            post.save()

    def download(self):
        posts = Post.objects.all()
        image_urls = set()

        for post in posts:
            page_element = html.fromstring(post.content)
            image_selector = CSSSelector('img')
            images = image_selector(page_element)
            for image in images:
                image_urls.add(image.attrib['src'])

        with open(self.url_image_mapping_file, 'w') as f:
            for url in self.urls:#image_urls:
                if url.startswith('http'):
                    try:
                        filename = self.download_and_save(url)
                        mapping[url] = filename
                        f.write("%s -> %s" % (url, filename))
                        f.write('\n')
                    except:
                        exc_type, exc_value, exc_traceback = sys.exc_info()
                        print url, exc_type, exc_value, traceback.format_tb(exc_traceback)
                        f.write("Failed to download %s" % url)
                        f.write('\n')

    def download_and_save(self, url, times=0):
        if times > 20:
            raise Exception('Failed to download after 19 reties')
        try:
            if url.startswith('https'):
                url = url.replace('https', 'http')
            req = urllib2.urlopen(url)
            mime = req.info().gettype()
            if mime == 'image/jpeg':
                ext = '.jpg'
            elif mime == 'image/gif':
                ext = '.gif'
            else:
                ext = ''
            self.m.update(url)
            filename = self.m.hexdigest() + ext
            self.save_image(filename, req.read())
            return filename
        except urllib2.HTTPError, urllib2.URLError:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print url, exc_type, exc_value, traceback.format_tb(exc_traceback)
            return self.download_and_save(url, times + 1)
    
    def save_image(self, filename, content):
        if not os.path.exists(self.image_folder):
            os.makedirs(self.image_folder)
        with open(os.path.join(self.image_folder, filename), 'w') as f:
            f.write(content)
