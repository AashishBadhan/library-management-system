from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# from .models import CustomUser

# CustomUser admin temporarily disabled
# @admin.register(CustomUser)
# class CustomUserAdmin(UserAdmin):
#     list_display = ['username', 'email', 'role', 'is_staff', 'is_active']
#     list_filter = ['role', 'is_staff', 'is_active']
#     fieldsets = UserAdmin.fieldsets + (
#         ('Additional Info', {'fields': ('phone_number', 'address', 'role', 'profile_picture')}),
#     )
#     add_fieldsets = UserAdmin.add_fieldsets + (
#         ('Additional Info', {'fields': ('phone_number', 'address', 'role')}),
#     )
