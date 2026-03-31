from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Department, Subject

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('subject_name', 'subject_id', 'subject_department', 'department')
    search_fields = ('subject_name', 'subject_id', 'subject_department', 'department__department_name')
    list_filter = ('subject_department', 'department')
    readonly_fields = ('slug',)
    fieldsets = (
        ('Subject Information', {'fields': ('subject_name', 'subject_id', 'subject_department')}),
        ('Department', {'fields': ('department',)}),
        ('Media', {'fields': ('subject_image',)}),
        ('System', {'fields': ('slug',)}),
    )
    actions = ['delete_selected']