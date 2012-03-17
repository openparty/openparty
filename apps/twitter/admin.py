from django.contrib import admin

from models import Tweet

class Tweet_Admin(admin.ModelAdmin):
    list_display = ('tweet_user_name', 'text', 'created_at', 'source')
    list_filter = ['source']

admin.site.register(Tweet, Tweet_Admin)
