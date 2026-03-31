from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.contrib import messages
from school.utils import create_notification

# Create your views here.

def add_department(request):
    if request.method == "POST":
        department_name = request.POST.get("department_name")
        department_id = request.POST.get("department_id")
        department_email = request.POST.get("department_email")
        mobile_number = request.POST.get("mobile_number")
        department_image = request.FILES.get("department_image")
        
        #retrive hod information
        hod_name = request.POST.get("hod_name")
        hod_mobile = request.POST.get("hod_mobile")
        hod_email = request.POST.get("hod_email")
        
        # save hod information to database
        hod = Hod.objects.create(
            hod_name=hod_name,
            hod_mobile=hod_mobile,
            hod_email=hod_email,
        )
        # save department information to database
        department = Department.objects.create(
            department_name=department_name,
            department_id=department_id,
            mobile_number=mobile_number,
            department_email = department_email,
            department_image=department_image,
            hod=hod,
        )
        messages.success(request, "Department added successfully!")
        # Create notification
        create_notification(request.user, f"Added Department: {department_name}")
        # return render(request, "department_list")
        # Process the form data as needed   
    return render(request, "departments/add-department.html")


def department_list(request):
    department_list = Department.objects.select_related('hod').all()
    context = {
        'department_list': department_list
    }
    return render(request, "departments/departments.html", context)




def edit_department(request, slug):
    department = get_object_or_404(Department, slug=slug)
    hod = department.hod if hasattr(department, 'hod') else None
    if request.method == "POST":
        department_name = request.POST.get("department_name")
        department_id = request.POST.get("department_id")
        mobile_number = request.POST.get("mobile_number")
        department_image = request.FILES.get("department_image")
        department_email = request.POST.get("department_email")
        
        #retrive hod information
        hod.hod_name = request.POST.get("hod_name")
        hod.hod_mobile = request.POST.get("hod_mobile")
        hod.hod_email = request.POST.get("hod_email")
        
        hod.save()
        
       
        department.department_name=department_name
        department.department_id=department_id
        department.mobile_number=mobile_number
        department.department_image=department_image
        department.department_email=department_email
        department.save()
        
        # Create notification
        create_notification(request.user, f"Updated Department: {department_name}")
        return redirect("department_list")
    return render(request, "departments/edit-department.html", {'department': department, 'hod': hod})

def department_details(request):
    return render(request, "departments/department-details.html")

def view_department(request, slug):
    department = get_object_or_404(Department, department_id = slug)
    context ={
        'department': department
    }
    return render(request, "departments/department-details.html", context)



def delete_department(request, slug):
    if request.method == "POST":
        department = get_object_or_404(Department, slug = slug)
        department_name = f"{department.department_name}"
        department.delete()
        
        # Create notification
        create_notification(request.user, f"Deleted department: {department_name}")
        return redirect("department_list")
    return HttpResponseForbidden()
    