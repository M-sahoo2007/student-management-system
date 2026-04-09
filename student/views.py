from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404,redirect
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User
from school.models import Notification
from school.utils import create_notification
from django.utils import timezone
from django.db.models import Q





# Create your views here.

def add_student(request):
    if request.user.is_authenticated and request.user.is_student:
        return HttpResponseForbidden("Students are not allowed to add students.")

    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        student_id = request.POST.get('student_id')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        student_class = request.POST.get('student_class')
        religion = request.POST.get('religion')
        joining_date = request.POST.get('joining_date')
        mobile_number = request.POST.get('mobile_number')
        admission_number = request.POST.get('admission_number')
        section = request.POST.get('section')
        student_image = request.FILES.get('student_image')

        # Retrieve parent data from the form
        father_name = request.POST.get('father_name')
        father_occupation = request.POST.get('father_occupation')
        father_mobile = request.POST.get('father_mobile')
        father_email = request.POST.get('father_email')
        mother_name = request.POST.get('mother_name')
        mother_occupation = request.POST.get('mother_occupation')
        mother_mobile = request.POST.get('mother_mobile')
        mother_email = request.POST.get('mother_email')
        present_address = request.POST.get('present_address')
        permanent_address = request.POST.get('permanent_address')

        # save parent information
        parent = Parent.objects.create(
            father_name= father_name,
            father_occupation= father_occupation,
            father_mobile= father_mobile,
            father_email= father_email,
            mother_name= mother_name,
            mother_occupation= mother_occupation,
            mother_mobile= mother_mobile,
            mother_email= mother_email,
            present_address= present_address,
            permanent_address= permanent_address
        )

        # Save student information
        student = Student.objects.create(
            first_name= first_name,
            last_name= last_name,
            student_id= student_id,
            gender= gender,
            date_of_birth= date_of_birth,
            student_class= student_class,
            religion= religion,
            joining_date= joining_date,
            mobile_number = mobile_number,
            admission_number = admission_number,
            section = section,
            student_image = student_image,
            parent = parent
        )
        create_notification(request.user, f"Added Student: {student.first_name} {student.last_name}")
        messages.success(request, "Student added Successfully")
        return redirect("student_list")

  

    return render(request,"students/add-student.html")



def student_list(request):
    student_list = Student.objects.select_related('parent').all()
    unread_notification = Notification.objects.filter(user=request.user, is_read=False) if request.user.is_authenticated else []
    context = {
        'student_list': student_list,
        'unread_notification': unread_notification
    }
    return render(request, "students/students.html", context)


def edit_student(request,slug):
    if request.user.is_authenticated and request.user.is_student:
        return HttpResponseForbidden("Students are not allowed to edit student records.")

    student = get_object_or_404(Student, slug=slug)
    parent = student.parent if hasattr(student, 'parent') else None
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        student_id = request.POST.get('student_id')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        student_class = request.POST.get('student_class')
        religion = request.POST.get('religion')
        joining_date = request.POST.get('joining_date')
        mobile_number = request.POST.get('mobile_number')
        admission_number = request.POST.get('admission_number')
        section = request.POST.get('section')
        student_image = request.FILES.get('student_image')  if request.FILES.get('student_image') else student.student_image

        # Retrieve parent data from the form
        parent.father_name = request.POST.get('father_name')
        parent.father_occupation = request.POST.get('father_occupation')
        parent.father_mobile = request.POST.get('father_mobile')
        parent.father_email = request.POST.get('father_email')
        parent.mother_name = request.POST.get('mother_name')
        parent.mother_occupation = request.POST.get('mother_occupation')
        parent.mother_mobile = request.POST.get('mother_mobile')
        parent.mother_email = request.POST.get('mother_email')
        parent.present_address = request.POST.get('present_address')
        parent.permanent_address = request.POST.get('permanent_address')
        parent.save()

#  update student information

        student.first_name= first_name
        student.last_name= last_name
        student.student_id= student_id
        student.gender= gender
        student.date_of_birth= date_of_birth
        student.student_class= student_class
        student.religion= religion
        student.joining_date= joining_date
        student.mobile_number = mobile_number
        student.admission_number = admission_number
        student.section = section
        student.student_image = student_image
        student.save()
        create_notification(request.user, f"Updated Student: {student.first_name} {student.last_name}")
        
        return redirect("student_list")
    return render(request, "students/edit-student.html",{'student':student, 'parent':parent} )


def view_student(request, slug):
    student = get_object_or_404(Student, student_id = slug)
    learning_history = LearningHistory.objects.filter(student=student).order_by('-start_datetime')[:10]
    context = {
        'student': student,
        'learning_history': learning_history
    }
    return render(request, "students/student-details.html", context)


def delete_student(request,slug):
    if request.user.is_authenticated and request.user.is_student:
        return HttpResponseForbidden("Students are not allowed to delete student records.")

    if request.method == "POST":
        student = get_object_or_404(Student, slug=slug)
        student_name = f"{student.first_name} {student.last_name}"
        student.delete()
        create_notification(request.user, f"Deleted student: {student_name}")
        return redirect ('student_list')
    return HttpResponseForbidden()

def student_dashboard(request):
    """Student dashboard view"""
    if not request.user.is_authenticated or not request.user.is_student:
        return redirect('index')
    
    # Get student data
    student = None
    try:
        student = Student.objects.filter(first_name=request.user.first_name, last_name=request.user.last_name).first()
    except:
        pass
    
    # Get statistics
    total_students = Student.objects.count()
    total_classes = len(set(Student.objects.values_list('student_class', flat=True)))
    total_subjects = 0  # Can be updated if Subject model exists

    today_courses = []
    learning_history = []
    calendar_events = []
    dashboard_stat = None
    if student:
        today_courses = CourseProgress.objects.filter(
            student_class=student.student_class,
            section=student.section
        ).order_by('start_time')[:2]
        learning_history = LearningHistory.objects.filter(student=student).order_by('-start_datetime')[:4]
        calendar_events = CalendarEvent.objects.filter(student=student).order_by('start_datetime')[:5]
        if today_courses:
            current = today_courses[0]
            dashboard_stat = {
                'completed': current.completed_lessons,
                'total': current.total_lessons,
                'status': current.status,
                'percent': current.progress_percent,
            }

    unread_notification = Notification.objects.filter(user=request.user, is_read=False)
    
    active_assignments = []
    assignment_history = []
    
    if student:
        # Auto-assign new assignments from teacher if not already assigned
        all_class_assignments = Assignment.objects.filter(
            student_class=student.student_class,
            section=student.section
        )
        for assignment in all_class_assignments:
            StudentAssignment.objects.get_or_create(
                student=student,
                assignment=assignment,
                defaults={'status': 'Not Started'}
            )
        
        # Get active assignments (not completed)
        active_assignments = StudentAssignment.objects.filter(
            student=student
        ).exclude(
            status__in=['Completed']
        ).order_by('assignment__due_date')[:5]
        
        # Get assignment history (completed assignments)
        assignment_history = StudentAssignment.objects.filter(
            student=student,
            status='Completed'
        ).order_by('-assignment__due_date')[:5]
        
        # Calculate progress percentage for assignment history
        for assignment in assignment_history:
            if assignment.score and assignment.assignment.total_points:
                assignment.progress_percentage = int((assignment.score / assignment.assignment.total_points) * 100)
            else:
                assignment.progress_percentage = 0
    
    context = {
        'student': student,
        'total_students': total_students,
        'total_classes': total_classes,
        'total_subjects': total_subjects,
        'today_courses': today_courses,
        'dashboard_stat': dashboard_stat,
        'learning_history': learning_history,
        'calendar_events': calendar_events,
        'active_assignments': active_assignments,
        'assignment_history': assignment_history,
        'unread_notification': unread_notification,
        'unread_notification_count': unread_notification.count()
    }
    return render(request, "students/student-dashboard.html", context)
