from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count
from .models import *
from django.contrib import messages
from school.models import Notification
from school.utils import create_notification
from student.models import Student, Assignment, StudentAssignment, LearningHistory

# Create your views here.
def can_manage_teachers(user):
    """Helper to check if the user has administrative privileges to manage teachers."""
    return user.is_authenticated and getattr(user, 'is_admin', False) and not user.is_student and not user.is_teacher

def add_teacher(request):
    if not can_manage_teachers(request.user):
        messages.error(request, "You do not have permission to add teachers.")
        return redirect("teacher_list")

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        teacher_id = request.POST.get("teacher_id")
        teacher_email = request.POST.get("teacher_email")
        gender = request.POST.get("gender")
        date_of_birth = request.POST.get("date_of_birth")
        teacher_department = request.POST.get("teacher_department")
        religion = request.POST.get("religion")
        joining_date = request.POST.get("joining_date")
        mobile_number = request.POST.get("mobile_number")
        teacher_image = request.FILES.get("teacher_image")
        
        #retrive parent information
        father_name = request.POST.get("father_name")
        father_occupation = request.POST.get("father_occupation")
        father_mobile = request.POST.get("father_mobile")
        father_email = request.POST.get("father_email")
        mother_name = request.POST.get("mother_name")
        mother_occupation = request.POST.get("mother_occupation")
        mother_mobile = request.POST.get("mother_mobile")
        mother_email = request.POST.get("mother_email")
        present_address = request.POST.get("present_address")
        permanent_address = request.POST.get("permanent_address")
        
        # save parent information to database
        parent = Parent.objects.create(
            father_name=father_name,
            father_occupation=father_occupation,
            father_mobile=father_mobile,
            father_email=father_email,
            mother_name=mother_name,
            mother_occupation=mother_occupation,
            mother_mobile=mother_mobile,
            mother_email=mother_email,
            present_address=present_address,
            permanent_address=permanent_address
        )
        # save teacher information to database
        teacher = Teacher.objects.create(
            first_name=first_name,
            last_name=last_name,
            teacher_id=teacher_id,
            gender=gender,
            date_of_birth=date_of_birth,
            teacher_department=teacher_department,
            religion=religion,
            joining_date=joining_date,
            mobile_number=mobile_number,
            teacher_email = teacher_email,
            teacher_image=teacher_image,
            parent=parent,
        )
        messages.success(request, "Teacher added successfully!")
        # Create notification
        create_notification(request.user, f"Added Teacher: {first_name} {last_name}")
        return redirect("teacher_list")
    return render(request, "teachers/add-teacher.html")


def teacher_list(request):
    teacher_list = Teacher.objects.select_related('parent').all()
    context = {
        'teacher_list': teacher_list,
        'can_manage_teachers': can_manage_teachers(request.user)
    }
    return render(request, "teachers/teachers.html", context)




def edit_teacher(request, slug):
    if not can_manage_teachers(request.user):
        messages.error(request, "You do not have permission to edit teachers.")
        return redirect("teacher_list")

    teacher = get_object_or_404(Teacher, slug=slug)
    parent = teacher.parent if hasattr(teacher, 'parent') else None
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        teacher_id = request.POST.get("teacher_id")
        gender = request.POST.get("gender")
        date_of_birth = request.POST.get("date_of_birth")
        religion = request.POST.get("religion")
        joining_date = request.POST.get("joining_date")
        mobile_number = request.POST.get("mobile_number")
        teacher_image = request.FILES.get("teacher_image")
        teacher_email = request.POST.get("teacher_email")
        teacher_department = request.POST.get("teacher_department")
        
        #retrive parent information
        parent.father_name = request.POST.get("father_name")
        parent.father_occupation = request.POST.get("father_occupation")
        parent.father_mobile = request.POST.get("father_mobile")
        parent.father_email = request.POST.get("father_email")
        parent.mother_name = request.POST.get("mother_name")
        parent.mother_occupation = request.POST.get("mother_occupation")
        parent.mother_mobile = request.POST.get("mother_mobile")
        parent.mother_email = request.POST.get("mother_email")
        parent.present_address = request.POST.get("present_address")
        parent.permanent_address = request.POST.get("permanent_address")
        parent.save()
        
       
        teacher.first_name=first_name
        teacher.last_name=last_name
        teacher.teacher_id=teacher_id
        teacher.gender=gender
        teacher.date_of_birth=date_of_birth
        teacher.religion=religion
        teacher.joining_date=joining_date
        teacher.mobile_number=mobile_number
        teacher.teacher_image=teacher_image
        teacher.teacher_email=teacher_email
        teacher.teacher_department=teacher_department
        teacher.save()
        
        # Create notification
        create_notification(request.user, f"Updated Teacher: {first_name} {last_name}")
        return redirect("teacher_list")
    return render(request, "teachers/edit-teacher.html", {'teacher': teacher, 'parent': parent})

def teacher_details(request):
    return render(request, "teachers/teacher-details.html")

def view_teacher(request, slug):
    teacher = get_object_or_404(Teacher, teacher_id = slug)
    context ={
        'teacher': teacher,
        'can_manage_teachers': can_manage_teachers(request.user)
    }
    return render(request, "teachers/teacher-details.html", context)



def delete_teacher(request, slug):
    if not can_manage_teachers(request.user):
        messages.error(request, "You do not have permission to delete teachers.")
        return redirect("teacher_list")

    if request.method == "POST":
        teacher = get_object_or_404(Teacher, slug = slug)
        teacher_name = f"{teacher.first_name} {teacher.last_name}"
        teacher.delete()
        
        # Create notification
        create_notification(request.user, f"Deleted teacher: {teacher_name}")
        return redirect("teacher_list")
    return HttpResponseForbidden()


def teacher_dashboard(request):
    """Teacher dashboard view"""
    if not request.user.is_authenticated:
        return redirect('index')
    
    # Get teacher data
    teacher = None
    try:
        teacher = Teacher.objects.filter(first_name=request.user.first_name, last_name=request.user.last_name).first()
    except:
        pass
    
    # Get statistics
    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()
    total_classes = len(set(Student.objects.values_list('student_class', flat=True)))
    total_subjects = 0  # Can be updated if Subject model exists
    recent_classes = (
        Student.objects.values('student_class', 'section')
        .annotate(student_count=Count('id'))
        .order_by('-student_count')[:5]
    )
    
    # Fetch recent assignments created by teachers
    recent_assignments = Assignment.objects.all().order_by('-created_at')[:5]
    
    # Fetch pending student submissions
    pending_submissions = StudentAssignment.objects.exclude(status='Completed').order_by('assignment__due_date')[:10]
    
    # Fetch recent learning/lesson history
    learning_history = LearningHistory.objects.all().order_by('-start_datetime')[:5]
    
    unread_notification = Notification.objects.filter(user=request.user, is_read=False)
    context = {
        'teacher': teacher,
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_classes': total_classes,
        'total_subjects': total_subjects,
        'recent_classes': recent_classes,
        'recent_assignments': recent_assignments,
        'pending_submissions': pending_submissions,
        'learning_history': learning_history,
        'unread_notification': unread_notification,
        'unread_notification_count': unread_notification.count()
    }
    return render(request, "teachers/teacher-dashboard.html", context)

def add_assignment(request):
    if not request.user.is_authenticated or request.user.is_student:
        return HttpResponseForbidden("Only teachers and admins can add assignments.")
    
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        student_class = request.POST.get("student_class")
        section = request.POST.get("section")
        due_date = request.POST.get("due_date")
        due_time = request.POST.get("due_time")
        total_points = request.POST.get("total_points") or 100
        
        Assignment.objects.create(
            title=title,
            description=description,
            student_class=student_class,
            section=section,
            due_date=due_date,
            due_time=due_time,
            created_by=request.user.get_full_name() or request.user.username,
            total_points=total_points
        )
        messages.success(request, "Assignment added successfully!")
        create_notification(request.user, f"Added Assignment: {title} for {student_class}-{section}")
        return redirect("teacher_dashboard")
        
    return render(request, "teachers/add-assignment.html")

def mark_submission_completed(request, submission_id):
    if not request.user.is_authenticated or request.user.is_student:
        return HttpResponseForbidden("Only teachers can mark assignments as completed.")
    
    submission = get_object_or_404(StudentAssignment, id=submission_id)
    submission.status = 'Completed'
    submission.score = submission.assignment.total_points  # Give full points
    submission.save()
    messages.success(request, f"Assignment '{submission.assignment.title}' for {submission.student.first_name} marked as completed!")
    create_notification(request.user, f"Marked assignment '{submission.assignment.title}' as completed for {submission.student.first_name}")
    return redirect('teacher_dashboard')
    