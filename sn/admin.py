from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from sn.models import Muppet

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class MuppetInline(admin.StackedInline):
    model = Muppet
    can_delete = False
    verbose_name_plural = 'muppet'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (MuppetInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
