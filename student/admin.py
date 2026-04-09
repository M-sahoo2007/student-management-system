from django.contrib import admin

# Register your models here.
from .models import Parent, Student, CourseProgress, LearningHistory, CalendarEvent, Assignment, StudentAssignment

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


@admin.register(CourseProgress)
class CourseProgressAdmin(admin.ModelAdmin):
    list_display = ('title', 'student_class', 'section', 'completed_lessons', 'total_lessons', 'progress_percent')
    search_fields = ('title', 'student_class', 'section')
    list_filter = ('status', 'student_class', 'section')
    fieldsets = (
        ('Course Information', {'fields': ('title', 'status')}),
        ('Class & Section', {'fields': ('student_class', 'section')}),
        ('Progress', {'fields': ('completed_lessons', 'total_lessons', 'progress_percent')}),
        ('Schedule', {'fields': ('start_time', 'end_time', 'duration_minutes')}),
        ('Assignments', {'fields': ('assignment_count',)}),
    )


@admin.register(LearningHistory)
class LearningHistoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'student', 'start_datetime', 'end_datetime', 'status')
    search_fields = ('title', 'student__first_name', 'student__last_name')
    list_filter = ('status',)


@admin.register(CalendarEvent)
class CalendarEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'student', 'start_datetime', 'end_datetime', 'color_class')
    search_fields = ('title', 'student__first_name', 'student__last_name')
    list_filter = ('color_class',)


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'student_class', 'section', 'due_date', 'due_time', 'created_by')
    search_fields = ('title', 'student_class', 'section', 'created_by')
    list_filter = ('student_class', 'section', 'due_date')
    fieldsets = (
        ('Assignment Details', {'fields': ('title', 'description', 'total_points')}),
        ('Class & Section', {'fields': ('student_class', 'section')}),
        ('Deadline', {'fields': ('due_date', 'due_time')}),
        ('Created By', {'fields': ('created_by',)}),
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(StudentAssignment)
class StudentAssignmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'assignment', 'status', 'submission_date', 'score')
    search_fields = ('student__first_name', 'student__last_name', 'assignment__title')
    list_filter = ('status', 'assignment__due_date')
    fieldsets = (
        ('Assignment', {'fields': ('student', 'assignment')}),
        ('Status', {'fields': ('status', 'submission_date')}),
        ('Grading', {'fields': ('score', 'feedback')}),
    )
    readonly_fields = ('assigned_at', 'updated_at')

