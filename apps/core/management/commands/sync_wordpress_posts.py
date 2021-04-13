#!/usr/bin/env python
# encoding: utf-8
import sys
from django.conf import settings
from django.core.management.base import BaseCommand
import MySQLdb
from collections import namedtuple

from apps.core.models import Post
from apps.member.models import Member


class Command(BaseCommand):
    row_structure = namedtuple(
        "Row",
        "id post_content post_title post_excerpt post_status post_name to_ping post_date post_modified guid post_author comment_count",
    )

    def handle(self, *args, **options):
        print "Start syncing"
        conn = MySQLdb.connect(
            host="localhost",
            user="root",
            db="openparty",
            use_unicode=True,
            charset="utf8",
        )
        cursor = conn.cursor()
        sql = "SELECT id, post_content, post_title, post_excerpt, post_status, post_name, to_ping, post_date, post_modified, guid, post_author, comment_count FROM wp_posts WHERE post_type = 'post' AND post_status = 'publish'"
        cursor.execute(sql)
        rows = cursor.fetchall()
        cleverpig = self.find_cleverpig()
        synced = 0
        for row in rows:
            rs = self.row_structure._make(row)
            if self.should_sync(rs):
                post = Post(
                    content=rs.post_content,
                    content_type="html",
                    title=rs.post_title,
                    summary=rs.post_excerpt,
                    status=10,
                    post_name=rs.post_name,
                    to_ping=rs.to_ping,
                    created_at=rs.post_date,
                    modified_at=rs.post_modified,
                    guid=rs.guid,
                    author="wp_%s" % rs.post_author,
                    created_by=cleverpig,
                    comment_count=rs.comment_count,
                )
                post.save()
                print "wp %s -> %s" % (rs.id, post.id)
                synced += 1

        print "Synced %s wordpress posts" % synced

    def should_sync(self, rs):
        return not len(Post.objects.filter(guid=rs.guid))  # not duplicate

    def find_cleverpig(self):
        return Member.objects.get(id=6)
