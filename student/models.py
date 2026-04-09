from django.db import models
from django.utils.text import slugify
from django.utils.crypto import get_random_string
from django.utils import timezone
# Create your models here.

from django.db import models

class Parent(models.Model):
    father_name = models.CharField(max_length=100)
    father_occupation = models.CharField(max_length=100, blank=True)
    father_mobile = models.CharField(max_length=15)
    father_email = models.EmailField(max_length=100)
    mother_name = models.CharField(max_length=100)
    mother_occupation = models.CharField(max_length=100, blank=True)
    mother_mobile = models.CharField(max_length=15)
    mother_email = models.EmailField(max_length=100)
    present_address = models.TextField()
    permanent_address = models.TextField()

    def __str__(self):
        return f"{self.father_name} & {self.mother_name}"

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=20)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')])
    date_of_birth = models.DateField()
    student_class = models.CharField(max_length=50)
    religion = models.CharField(max_length=50)
    joining_date = models.DateField()
    mobile_number = models.CharField(max_length=15)
    admission_number = models.CharField(max_length=20)
    section = models.CharField(max_length=10)
    student_image = models.ImageField(upload_to='students/', blank=True)
    parent = models.OneToOneField(Parent, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.first_name}-{self.last_name}-{self.student_id}")
        super(Student, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"


class CourseProgress(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='course_progress', null=True, blank=True)
    title = models.CharField(max_length=200)
    student_class = models.CharField(max_length=50, default='Class 10')
    section = models.CharField(max_length=10, default='A')
    completed_lessons = models.PositiveIntegerField(default=0)
    total_lessons = models.PositiveIntegerField(default=0)
    start_time = models.TimeField()
    end_time = models.TimeField()
    duration_minutes = models.PositiveIntegerField(default=0)
    assignment_count = models.PositiveIntegerField(default=0)
    progress_percent = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=50, default='Lesson Learned')

    def __str__(self):
        return f"{self.title} ({self.student_class}-{self.section})"


class LearningHistory(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='learning_history')
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    title = models.CharField(max_length=200)
    duration_minutes = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=50, choices=[('In Progress', 'In Progress'), ('Completed', 'Completed')], default='In Progress')

    def __str__(self):
        return f"{self.title} ({self.status})"


class CalendarEvent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='calendar_events')
    title = models.CharField(max_length=200)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    color_class = models.CharField(max_length=50, default='calendar-blue')

    def __str__(self):
        return f"{self.title} ({self.start_datetime})"


class Assignment(models.Model):
    """Teacher-created assignments for a specific class/section"""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    student_class = models.CharField(max_length=50)
    section = models.CharField(max_length=10)
    due_date = models.DateField()
    due_time = models.TimeField()
    created_by = models.CharField(max_length=100)  # Teacher name or ID
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_points = models.PositiveIntegerField(default=100)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.student_class}-{self.section})"


class StudentAssignment(models.Model):
    """Student assignment completion tracking"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='assignments')
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='student_submissions')
    status = models.CharField(
        max_length=50,
        choices=[
            ('Not Started', 'Not Started'),
            ('In Progress', 'In Progress'),
            ('Submitted', 'Submitted'),
            ('Completed', 'Completed'),
            ('Late', 'Late'),
        ],
        default='Not Started'
    )
    submission_date = models.DateTimeField(null=True, blank=True)
    score = models.PositiveIntegerField(null=True, blank=True)
    feedback = models.TextField(blank=True)
    assigned_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'assignment')
        ordering = ['-assignment__due_date']

    def __str__(self):
        return f"{self.student} - {self.assignment.title}"
