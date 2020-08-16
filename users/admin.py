from django.contrib import admin
from django.contrib.auth.models import Group
from users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
