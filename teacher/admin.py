from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Parent, Teacher

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('father_name', 'mother_name', 'father_mobile', 'mother_mobile')
    search_fields = ('father_name', 'mother_name', 'father_mobile', 'mother_mobile')
    list_filter = ('father_name','mother_name')
    
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'teacher_id', 'gender', 'date_of_birth', 'teacher_department', 'joining_date', 'mobile_number')
    search_fields = ('first_name', 'last_name', 'teacher_id', 'teacher_department', 'teacher_email')
    list_filter = ('gender', 'teacher_department', 'joining_date')
    readonly_fields = ('slug',)
    fieldsets = (
        ('Personal Information', {'fields': ('first_name', 'last_name', 'gender', 'date_of_birth', 'religion')}),
        ('Teacher Details', {'fields': ('teacher_id', 'teacher_department', 'joining_date')}),
        ('Contact', {'fields': ('mobile_number', 'teacher_email', 'parent')}),
        ('Media', {'fields': ('teacher_image',)}),
        ('System', {'fields': ('slug',)}),
    )
    actions = ['delete_selected']