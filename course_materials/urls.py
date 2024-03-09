from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('', views.home, name='home'),

    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='elearningapp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('dashboard/', views.dashboard_redirect, name='dashboard_redirect'),

    path('teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('create_course/', views.create_course, name='create_course'),
    path('edit_course/<int:course_id>/', views.edit_course, name='edit_course'),
    path('delete_course/<int:course_id>/', views.delete_course, name='delete_course'),

    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),


]
