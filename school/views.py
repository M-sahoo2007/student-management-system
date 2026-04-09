from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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
    
    if request.method == 'POST':
        # Update base user fields
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()
        
        mobile_number = request.POST.get('mobile_number')
        profile_image = request.FILES.get('profile_image')
        
        # Update student record if the user is a student
        if student:
            student.first_name = user.first_name
            student.last_name = user.last_name
            if mobile_number:
                student.mobile_number = mobile_number
            if profile_image:
                student.student_image = profile_image
            student.save()
            
        # Update teacher record if the user is a teacher
        if teacher:
            teacher.first_name = user.first_name
            teacher.last_name = user.last_name
            teacher.teacher_email = user.email
            if mobile_number:
                teacher.mobile_number = mobile_number
            if profile_image:
                teacher.teacher_image = profile_image
            teacher.save()
            
        messages.success(request, 'Your profile has been updated successfully!')
        return redirect('profile')

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