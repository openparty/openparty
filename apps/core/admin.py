from django.contrib import admin

from models import Event, Topic
from models import Favorite, Vote

class Event_Admin(admin.ModelAdmin):
    list_display = ('name', 'begin_time')
    list_filter = ['begin_time']

admin.site.register(Event, Event_Admin)

class Topic_Admin(admin.ModelAdmin):
	list_display = ('name', 'author', 'total_votes', 'in_event', 'accepted')
	#list_filter = ['total_votes', 'author', 'in_event', 'accepted']

admin.site.register(Topic, Topic_Admin)

#admin.site.register(Topic)
#admin.site.register(Event)

admin.site.register(Favorite)
admin.site.register(Vote)
