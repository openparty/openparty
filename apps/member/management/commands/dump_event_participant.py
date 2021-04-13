# -*- coding: utf-8 -*-
import sys
import csv
from django.conf import settings
from django.core.management.base import BaseCommand

from apps.member.forms import ProfileForm
from apps.core.models import Event


class Command(BaseCommand):
    def handle(self, *args, **options):
        if len(args):
            event_id = int(args[0])
            event = Event.objects.get(pk=event_id)
        else:
            event = Event.objects.next_event()
        csv_file_name = "/tmp/openparty_%s_participants.csv" % event.id
        writer = csv.writer(open(csv_file_name, "w"))
        header = (
            "id",
            "username",
            "nickname",
            "realname",
            "gender",
            "career",
            "company",
            "position",
            "blog",
            "phone",
            "hobby",
            "gtalk",
            "msn",
            "twitter",
            "foursquare",
        )
        writer.writerow(header)
        for member in event.participants.all():
            profile = ProfileForm(user=member.user).data

            def prop(prop_name):
                try:
                    return unicode(profile.get(prop_name, ""), "utf8").encode("utf8")
                except UnicodeDecodeError:
                    return ""

            row = (
                member.id,
                member.user.username.encode("utf8"),
                member.nickname.encode("utf8"),
                prop("realname"),
                prop("gender"),
                prop("career_years"),
                prop("company"),
                prop("position"),
                prop("blog"),
                prop("phone"),
                prop("hobby"),
                prop("gtalk"),
                prop("msn"),
                prop("twitter"),
                prop("foursquare"),
            )
            writer.writerow(row)
        print "out put csv file to %s" % csv_file_name
