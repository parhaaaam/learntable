from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Role, ExtendedPermission

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'name', 'is_staff', 'is_active', 'is_email_verified')
    list_filter = ('is_staff', 'is_active', 'gender', 'groups')
    search_fields = ('email', 'name')
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('name', 'gender', 'birth')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined', 'email_verified_at')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2'),
        }),
    )

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'name', 'description', 'created_at')
    search_fields = ('display_name', 'name', 'description')
    list_filter = ('created_at',)
    ordering = ('display_name',)
    
    def name(self, obj):
        return obj.group.name
    
    fieldsets = (
        (None, {
            'fields': ('group', 'display_name', 'description')
        }),
    )

@admin.register(ExtendedPermission)
class ExtendedPermissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'codename', 'content_type', 'description')
    search_fields = ('permission__name', 'permission__codename', 'description')
    list_filter = ('permission__content_type',)
    ordering = ('permission__content_type', 'permission__codename')
    
    def name(self, obj):
        return obj.permission.name
    
    def codename(self, obj):
        return obj.permission.codename
    
    def content_type(self, obj):
        return obj.permission.content_type 