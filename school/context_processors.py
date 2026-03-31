from .models import Notification
from student.models import Student
from teacher.models import Teacher

def notifications(request):
    """
    Context processor that adds notification data to all templates.
    """
    if request.user.is_authenticated:
        unread_notification = Notification.objects.filter(user=request.user, is_read=False)
        unread_notification_count = unread_notification.count()
        return {
            'unread_notification': unread_notification,
            'unread_notification_count': unread_notification_count
        }
    return {
        'unread_notification': [],
        'unread_notification_count': 0
    }

def user_profile(request):
    """
    Context processor that adds user profile data (student/teacher) to all templates.
    """
    student = None
    teacher = None
    
    if request.user.is_authenticated:
        # Try to get student profile (search by first and last name)
        try:
            student = Student.objects.filter(
                first_name=request.user.first_name, 
                last_name=request.user.last_name
            ).first()
        except:
            pass
        
        # Try to get teacher profile (search by first and last name)
        try:
            teacher = Teacher.objects.filter(
                first_name=request.user.first_name, 
                last_name=request.user.last_name
            ).first()
        except:
            pass
    
    return {
        'student': student,
        'teacher': teacher,
    }
