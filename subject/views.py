from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.contrib import messages
from school.utils import create_notification

# Helper function to check if user is a student
def is_student(user):
    return user.is_authenticated and user.is_student

# Create your views here.

def add_subject(request):
    # Prevent students from adding subjects
    if is_student(request.user):
        messages.error(request, "Students do not have permission to add subjects.")
        return redirect("subject_list")
    if request.method == "POST":
        subject_name = request.POST.get("subject_name")
        subject_id = request.POST.get("subject_id")
        subject_image = request.FILES.get("subject_image")
        
        #retrive department information
        department_name = request.POST.get("department_name")
        department_email = request.POST.get("department_email")
        # department_id = request.POST.get("department_id")
        
        # save department information to database
        department = Department.objects.create(
            department_name=department_name,
            department_email=department_email,
        )
        # save subject information to database
        subject = Subject.objects.create(
            subject_name=subject_name,
            subject_id=subject_id,
            subject_image=subject_image,
            department=department,
        )
        messages.success(request, "Subject added successfully!")
        # Create notification
        create_notification(request.user, f"Added Subject: {subject_name}")
        # return render(request, "subject_list")
        # Process the form data as needed   
    return render(request, "subjects/add-subject.html")


def subject_list(request):
    subject_list = Subject.objects.select_related('department').all()
    context = {
        'subject_list': subject_list
    }
    return render(request, "subjects/subjects.html", context)




def edit_subject(request, slug):
    # Prevent students from editing subjects
    if is_student(request.user):
        messages.error(request, "Students do not have permission to edit subjects.")
        return redirect("subject_list")
    subject = get_object_or_404(Subject, slug=slug)
    department = subject.department if hasattr(subject, 'department') else None
    if request.method == "POST":
        subject_name = request.POST.get("subject_name")
        subject_id = request.POST.get("subject_id")
        subject_image = request.FILES.get("subject_image")
        
        #retrive department information
        department.department_name = request.POST.get("department_name")
        department.department_email = request.POST.get("department_email")
        department.save()
        
       
        subject.subject_name=subject_name
        subject.subject_id=subject_id
        subject.subject_image=subject_image
        
        subject.save()
        
        # Create notification
        create_notification(request.user, f"Updated Subject: {subject_name}")
        return redirect("subject_list")
    return render(request, "subjects/edit-subject.html", {'subject': subject, 'department' : department})

def subject_details(request):
    return render(request, "subjects/subject-details.html")

def view_subject(request, slug):
    subject = get_object_or_404(Subject, subject_id = slug)
    context ={
        'subject': subject
    }
    return render(request, "subjects/subject-details.html", context)


def delete_subject(request, slug):
    # Prevent students from deleting subjects
    if is_student(request.user):
        messages.error(request, "Students do not have permission to delete subjects.")
        return redirect("subject_list")
    if request.method == "POST":
        subject = get_object_or_404(Subject, slug = slug)
        subject_name = f"{subject.subject_name}"
        subject.delete()
        
        # Create notification
        create_notification(request.user, f"Deleted subject: {subject_name}")
        return redirect("subject_list")
    return HttpResponseForbidden()
    