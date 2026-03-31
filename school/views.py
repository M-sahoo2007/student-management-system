from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Notification
from student.models import Student
from teacher.models import Teacher

# Create your views here.

def index(request):
    return render(request, "authentication/login.html")

@login_required
def profile(request):
    """User profile page"""
    user = request.user
    student = None
    teacher = None
    
    # Try to get student or teacher profile
    if user.is_student:
        try:
            student = Student.objects.get(first_name=user.first_name)
        except Student.DoesNotExist:
            pass
    
    if user.is_teacher:
        try:
            teacher = Teacher.objects.get(first_name=user.first_name)
        except Teacher.DoesNotExist:
            pass
    
    context = {
        'user': user,
        'student': student,
        'teacher': teacher,
    }
    return render(request, "Home/profile.html", context)

@login_required
def inbox(request):
    """User inbox/messages page"""
    user = request.user
    notifications = Notification.objects.filter(user=user).order_by('-created_at')[:50]
    
    context = {
        'notifications': notifications,
    }
    return render(request, "Home/inbox.html", context)

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('index')
    
    # Get statistics
    total_students = Student.objects.count()
    total_classes = len(set(Student.objects.values_list('student_class', flat=True)))
    total_subjects = 0  # Can be updated if Subject model exists
    
    unread_notification = Notification.objects.filter(user=request.user, is_read=False)
    unread_notification_count = unread_notification.count()
    
    context = {
        'total_students': total_students,
        'total_classes': total_classes,
        'total_subjects': total_subjects,
        'unread_notification': unread_notification,
        'unread_notification_count': unread_notification_count
    }
    return render(request, "students/student-dashboard.html", context)


def admin_dashboard(request):
    """Admin dashboard view"""
    if not request.user.is_authenticated or not request.user.is_admin:
        return redirect('index')
    
    # Get statistics
    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()
    total_classes = len(set(Student.objects.values_list('student_class', flat=True)))
    total_departments = 0  # Can be updated if Department model exists
    
    unread_notification = Notification.objects.filter(user=request.user, is_read=False)
    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_classes': total_classes,
        'total_departments': total_departments,
        'unread_notification': unread_notification,
        'unread_notification_count': unread_notification.count()
    }
    return render(request, "school/admin-dashboard.html", context)




def mark_notification_as_read(request):
    if request.method == 'POST':
        notification = Notification.objects.filter(user=request.user, is_read=False)
        notification.update(is_read=True)
        return JsonResponse({'status': 'success'})
    return HttpResponseForbidden()

def clear_all_notification(request):
    if request.method == "POST":
        notification = Notification.objects.filter(user=request.user)
        notification.delete()
        return JsonResponse({'status': 'success'})
    return HttpResponseForbidden