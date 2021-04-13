#!/usr/bin/env python
# encoding: utf-8
from datetime import datetime, timedelta
from apps.core.models import Event
from apps.member import test_helper as member_test_helper


def yesterday():
    return datetime.now() - timedelta(days=1)


def the_day_before_yesterday():
    return datetime.now() - timedelta(days=2)


def tomorrow():
    return datetime.now() + timedelta(days=1)


def create_running_event(name="running event", content="running event"):
    event = Event(
        begin_time=yesterday(), end_time=tomorrow(), name=name, content=content
    )
    event.last_modified_by = member_test_helper.create_user()
    event.save()

    return event


def create_passed_event(name="passed event", content="passed event"):
    event = Event(
        begin_time=the_day_before_yesterday(),
        end_time=yesterday(),
        name=name,
        content=content,
    )
    event.last_modified_by = member_test_helper.create_user()
    event.save()

    return event


def create_upcoming_event(name="upcoming event", content="upcoming event"):
    event = Event(
        begin_time=tomorrow(), end_time=tomorrow(), name=name, content=content
    )
    event.last_modified_by = member_test_helper.create_user()
    event.save()

    return event
