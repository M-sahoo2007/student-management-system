from .models import Notification

def create_notification(user, message):
    """Create a notification for a user"""
    if user and user.is_authenticated:
        Notification.objects.create(user=user, message=message)
