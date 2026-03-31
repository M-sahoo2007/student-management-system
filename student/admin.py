from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Parent, Student

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('father_name', 'mother_name', 'father_mobile', 'mother_mobile', 'father_email')
    search_fields = ('father_name', 'mother_name', 'father_mobile', 'mother_mobile', 'father_email', 'mother_email')
    list_filter = ('father_name', 'mother_name')
    fieldsets = (
        ('Father Information', {'fields': ('father_name', 'father_mobile', 'father_email')}),
        ('Mother Information', {'fields': ('mother_name', 'mother_mobile', 'mother_email')}),
    )
    actions = ['delete_selected']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'student_id', 'gender', 'date_of_birth', 'student_class', 'joining_date', 'mobile_number', 'admission_number', 'section')
    search_fields = ('first_name', 'last_name', 'student_id', 'student_class', 'admission_number')
    list_filter = ('gender', 'student_class', 'section', 'joining_date')
    readonly_fields = ('slug',)
    fieldsets = (
        ('Personal Information', {'fields': ('first_name', 'last_name', 'gender', 'date_of_birth', 'religion')}),
        ('Student Details', {'fields': ('student_id', 'student_class', 'section', 'joining_date', 'admission_number')}),
        ('Contact', {'fields': ('mobile_number', 'parent')}),
        ('Media', {'fields': ('student_image',)}),
        ('System', {'fields': ('slug',)}),
    )
    actions = ['delete_selected']
