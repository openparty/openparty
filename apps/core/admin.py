from django.contrib import admin

from models import Event, Topic


class Event_Admin(admin.ModelAdmin):
    list_display = ('name', 'begin_time')
    list_filter = ['begin_time']

admin.site.register(Event, Event_Admin)

class Topic_Admin(admin.ModelAdmin):
	list_display = ('name', 'author', 'total_votes', 'in_event')
	list_filter = ['total_votes', 'author', 'in_event']

admin.site.register(Topic, Topic_Admin)

from models import Favorite, Vote, Comment
admin.site.register(Favorite)
admin.site.register(Vote)
admin.site.register(Comment)
