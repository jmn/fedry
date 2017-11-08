from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from fd.models import FeedSource
from django.db.models import Count

class FeedSourceInline(admin.TabularInline):
    model = FeedSource
    extra = 0 

class UserAdmin(BaseUserAdmin):
    inlines = (FeedSourceInline, )

admin.site.unregister(User)
# list filter has_feeds
class HasFeedsFilter(admin.SimpleListFilter):
    title = _('has feeds')
    parameter_name = 'has_feeds'
    def lookups(self, request, model_admin):
        return (
            ('true', _('Yes')),
            ('false', _('No')),
        )
    
    def queryset(self, request, queryset):
        if self.value() == 'true':
            return queryset.all().annotate(count= Count('feedsource')).filter(count__gt=0)
        if self.value() == 'false':
            return queryset.all().annotate(count= Count('feedsource')).filter(count__lt=1)
                    
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ['user_name', 'first_name', 'last_name', 'email', 'num_feeds']
    list_display = ('username', 'email', 'first_name', 'last_name', 'num_feeds')
    inlines = (FeedSourceInline, )
    list_filter = ('is_staff', HasFeedsFilter)

    def num_feeds(self, obj):
        return obj.feedsource_set.count()

    # def has_feeds(self, obj):
    #     if obj.feedsource_set.count > 0: return True
    #     else: return False
