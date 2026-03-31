from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Hod , Department

@admin.register(Hod)
class HodAdmin(admin.ModelAdmin):
    list_display = ('hod_name', 'hod_mobile', 'hod_email')
    search_fields = ('hod_name', 'hod_mobile', 'hod_email')
    list_filter = ('hod_name',)
    fieldsets = (
        ('HOD Information', {'fields': ('hod_name', 'hod_mobile', 'hod_email')}),
    )
    actions = ['delete_selected']
    
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('department_name', 'department_id', 'mobile_number', 'hod', 'department_email')
    search_fields = ('department_name', 'department_id', 'mobile_number', 'department_email')
    list_filter = ('department_id', 'hod')
    readonly_fields = ('slug',)
    fieldsets = (
        ('Department Information', {'fields': ('department_name', 'department_id')}),
        ('Contact', {'fields': ('mobile_number', 'department_email')}),
        ('Leadership', {'fields': ('hod',)}),
        ('Media', {'fields': ('department_image',)}),
        ('System', {'fields': ('slug',)}),
    )
    actions = ['delete_selected']