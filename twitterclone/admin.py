from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile
#unregister groups
admin.site.unregister(Group)
# mix profile and user
class ProfileInline(admin.StackedInline):
    model = Profile
    
# Extend User Model
class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username"]
    inlines = [ProfileInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Profile)