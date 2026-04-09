from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path("dashboard/", views.teacher_dashboard, name="teacher_dashboard"),
    path("", views.teacher_list, name="teacher_list"),
    path("add/", views.add_teacher, name="add_teacher"),
    path("add-assignment/", views.add_assignment, name="add_assignment"),
    path("mark-completed/<int:submission_id>/", views.mark_submission_completed, name="mark_submission_completed"),
    path('teachers/<str:slug>/', views.view_teacher,name='view_teacher'),
    path('edit/<str:slug>/', views.edit_teacher, name='edit_teacher'),
    path('delete/<str:slug>/', views.delete_teacher, name='delete_teacher'),
]
