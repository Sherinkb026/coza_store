from django.contrib import admin

# Register your models here.
from django.contrib import admin
from userauthentication.models import User


# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ['username','email','bio']

admin.site.register(User,UserAdmin)
