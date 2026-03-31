from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import CustomUser, PasswordResetRequest
from school.admin_actions import AdminActions

# Custom UserAdmin with conditional logic for superusers and staff
class CustomUserAdmin(DefaultUserAdmin):
    # Customize which fields are displayed in the admin form
    fieldsets = (
        (None, {'fields': ('username', 'password')}),  # Login details
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),  # Personal details
        ('Roles', {'fields': ('is_student', 'is_teacher', 'is_admin')}),  # Role fields
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_authorized',  # Add is_authorized here
                                    'groups', 'user_permissions')}),  # Admin permissions
    )

    # Customize fields in the user creation form (when creating a new user)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_authorized', 'is_student', 'is_teacher', 'is_admin')}
         ),
    )

    # Customize what fields are displayed in the list view
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'is_authorized',
        'is_student', 'is_teacher', 'is_admin', 'is_staff', 'is_superuser'
    )

    # Filter users based on role and authorization
    list_filter = ('is_student', 'is_teacher', 'is_admin', 'is_authorized', 'is_staff', 'is_superuser')
    
    # Search fields
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    # Actions
    actions = [
        'delete_selected',
        AdminActions.make_authorized,
        AdminActions.make_unauthorized,
        AdminActions.promote_to_admin,
        AdminActions.remove_admin_status,
    ]

    # Customize queryset to separate superusers and staff in the admin list view
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset  # Superusers see all users
        return queryset.filter(is_superuser=False)  # Non-superuser staff won't see superusers

# Register the CustomUser model with the custom admin
admin.site.register(CustomUser, CustomUserAdmin)

# Register PasswordResetRequest
@admin.register(PasswordResetRequest)
class PasswordResetRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'created_at', 'is_valid')
    search_fields = ('user__username', 'email')
    list_filter = ('created_at',)
    readonly_fields = ('token', 'created_at')
    fieldsets = (
        ('User Info', {'fields': ('user', 'email')}),
        ('Token', {'fields': ('token', 'created_at')}),
    )
    actions = ['delete_selected']
    
    def is_valid(self, obj):
        return obj.is_valid()
    is_valid.boolean = True
    is_valid.short_description = 'Token Valid'
