from django.contrib import admin

from models import Event, Topic

admin.site.register(Event)
admin.site.register(Topic)

from models import Fav, Vote, Comment
admin.site.register(Fav)
admin.site.register(Vote)
admin.site.register(Comment)
