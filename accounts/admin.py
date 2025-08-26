from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import CustomUser, Profile

@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "role", "location", "is_active", "is_staff")
    search_fields = ("email", "location")
    list_filter = ("role", "is_active", "is_staff")

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone_number")
    search_fields = ("user__email", "phone_number")