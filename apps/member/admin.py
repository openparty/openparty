from django.contrib import admin

from apps.member.models import Member

class Member_Admin(admin.ModelAdmin):
    raw_id_fields = ('user', )

admin.site.register(Member, Member_Admin)
