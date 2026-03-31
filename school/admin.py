from django.contrib import admin
from .models import Notification
from .admin_actions import AdminActions

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_read', 'created_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'message')
    list_filter = ('is_read', 'created_at')
    readonly_fields = ('id', 'created_at')
    fieldsets = (
        ('Notification Details', {'fields': ('user', 'message', 'is_read')}),
        ('Metadata', {'fields': ('id', 'created_at')}),
    )
    actions = [
        'delete_selected',
        AdminActions.mark_as_read,
        AdminActions.mark_as_unread,
    ]
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ['user', 'message']
        return self.readonly_fields