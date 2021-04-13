from django.contrib import admin

from .models import Event, Topic
from .models import Favorite, Vote
from .models import Post

class Event_Admin(admin.ModelAdmin):
    list_display = ('name', 'begin_time')
    list_filter = ['begin_time']
    raw_id_fields = ('participants', 'appearances', 'last_modified_by')
    ordering = ['-id']

admin.site.register(Event, Event_Admin)

class Topic_Admin(admin.ModelAdmin):
    list_display = ('name', 'author', 'total_votes', 'in_event', 'accepted')
    list_filter = ['in_event', 'accepted']
    raw_id_fields = ('author', 'in_event', 'last_modified_by', )
    ordering = ['-id']
    
admin.site.register(Topic, Topic_Admin)

class Post_Admin(admin.ModelAdmin):
    list_display = ('title','post_name')
    date_hierarchy='created_at'
    raw_id_fields = ('created_by', )
    ordering = ['-id']

admin.site.register(Post,Post_Admin)

class Vote_Fav_Admin(admin.ModelAdmin):
    raw_id_fields = ('user', )

admin.site.register(Vote, Vote_Fav_Admin)
admin.site.register(Favorite, Vote_Fav_Admin)


