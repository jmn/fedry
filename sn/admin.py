from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from sn.models import Muppet, Post
from fd.models import FeedSource

class FeedSourceInline(admin.TabularInline):
    model = FeedSource
    extra = 0 

class UserAdmin(BaseUserAdmin):
    inlines = (FeedSourceInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Post)
