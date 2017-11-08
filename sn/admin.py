from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from fd.models import FeedSource

class FeedSourceInline(admin.TabularInline):
    model = FeedSource
    extra = 0 

class UserAdmin(BaseUserAdmin):
    inlines = (FeedSourceInline, )

admin.site.unregister(User)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ['user_name', 'first_name', 'last_name', 'email', 'num_feeds']
    list_display = ('username', 'email', 'first_name', 'last_name', 'num_feeds')
    inlines = (FeedSourceInline, )
    list_filter = ('is_staff',)
    def num_feeds(self, obj):
        return obj.feedsource_set.count()
    
