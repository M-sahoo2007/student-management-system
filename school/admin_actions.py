from django.utils.html import format_html
from django.contrib import messages

class AdminActions:
    """Custom admin actions for enhanced functionality"""
    
    @staticmethod
    def make_active(modeladmin, request, queryset):
        """Mark selected items as active"""
        if hasattr(queryset.model, 'is_active'):
            count = queryset.update(is_active=True)
            messages.success(request, f'{count} item(s) marked as active.')
        else:
            messages.error(request, 'This model does not have an "is_active" field.')
    make_active.short_description = "✓ Mark selected as ACTIVE"
    
    @staticmethod
    def make_inactive(modeladmin, request, queryset):
        """Mark selected items as inactive"""
        if hasattr(queryset.model, 'is_active'):
            count = queryset.update(is_active=False)
            messages.success(request, f'{count} item(s) marked as inactive.')
        else:
            messages.error(request, 'This model does not have an "is_active" field.')
    make_inactive.short_description = "✗ Mark selected as INACTIVE"
    
    @staticmethod
    def make_authorized(modeladmin, request, queryset):
        """Mark selected users as authorized"""
        if hasattr(queryset.model, 'is_authorized'):
            count = queryset.update(is_authorized=True)
            messages.success(request, f'{count} item(s) marked as authorized.')
        else:
            messages.error(request, 'This model does not have an "is_authorized" field.')
    make_authorized.short_description = "✓ Mark selected as AUTHORIZED"
    
    @staticmethod
    def make_unauthorized(modeladmin, request, queryset):
        """Mark selected users as unauthorized"""
        if hasattr(queryset.model, 'is_authorized'):
            count = queryset.update(is_authorized=False)
            messages.success(request, f'{count} item(s) marked as unauthorized.')
        else:
            messages.error(request, 'This model does not have an "is_authorized" field.')
    make_unauthorized.short_description = "✗ Mark selected as UNAUTHORIZED"
    
    @staticmethod
    def mark_as_read(modeladmin, request, queryset):
        """Mark notifications as read"""
        if hasattr(queryset.model, 'is_read'):
            count = queryset.update(is_read=True)
            messages.success(request, f'{count} notification(s) marked as read.')
        else:
            messages.error(request, 'This model does not have an "is_read" field.')
    mark_as_read.short_description = "✓ Mark selected as READ"
    
    @staticmethod
    def mark_as_unread(modeladmin, request, queryset):
        """Mark notifications as unread"""
        if hasattr(queryset.model, 'is_read'):
            count = queryset.update(is_read=False)
            messages.success(request, f'{count} notification(s) marked as unread.')
        else:
            messages.error(request, 'This model does not have an "is_read" field.')
    mark_as_unread.short_description = "✗ Mark selected as UNREAD"

    @staticmethod
    def promote_to_admin(modeladmin, request, queryset):
        """Promote users to admin"""
        if hasattr(queryset.model, 'is_admin'):
            count = queryset.update(is_admin=True, is_staff=True, is_authorized=True)
            messages.success(request, f'{count} user(s) promoted to ADMIN.')
        else:
            messages.error(request, 'This model does not have admin fields.')
    promote_to_admin.short_description = "↑ Promote selected to ADMIN"

    @staticmethod
    def remove_admin_status(modeladmin, request, queryset):
        """Remove admin status from users"""
        if hasattr(queryset.model, 'is_admin'):
            count = queryset.update(is_admin=False, is_staff=False)
            messages.success(request, f'{count} user(s) removed from ADMIN status.')
        else:
            messages.error(request, 'This model does not have admin fields.')
    remove_admin_status.short_description = "↓ Remove ADMIN status"
