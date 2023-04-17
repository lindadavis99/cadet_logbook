from .models import Profile, Cadetlogbook
from django.contrib import admin


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'profile_pic', 'smart',  'account_type', 'profile_updated', 'created', 'updated', )
    list_display_links = ('id', 'user',)
#


@admin.register(Cadetlogbook)
class Cadetlogbook(admin.ModelAdmin):
    list_display = ('id', 'user', 'department', 'work_status', 'work_title',  'description_of_work', 'end_date', 'created', 'updated')
    list_display_links = ('id', 'user',)