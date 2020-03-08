from django.contrib import admin

# Register your models here.
from apps.users.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display =("id","username","nick_name")


admin.site.register(UserProfile,UserProfileAdmin)