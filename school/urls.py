from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
   path('',views.index, name="index"),
   path('dashboard/', views.dashboard, name='dashboard'),
   path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
   path('profile/', views.profile, name='profile'),
   path('inbox/', views.inbox, name='inbox'),
   path('notification/mark-as-read/', views.mark_notification_as_read, name='mark_notification_as_read' ),
   path('notification/clear-all', views.clear_all_notification, name= "clear_all_notification")


]
