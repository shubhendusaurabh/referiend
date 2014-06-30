from django.contrib import admin

from .models import UserProfile

def username(obj):
    return (obj.user.username)
username.short_description = 'User username'

def user_email(obj):
    return (obj.user.email)
user_email.short_description = 'User email'

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('email', username, user_email) #TODO social accounts
    search_fields = ('email', 'user__username', 'user__email')

admin.site.register(UserProfile, UserProfileAdmin)
