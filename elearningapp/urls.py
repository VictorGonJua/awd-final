from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.conf.urls.static import static




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
    path('edit_teacher_profile/', views.edit_teacher_profile, name='edit_teacher_profile'),
    path('search/', views.search_users, name='search_users'),
    path('user_profile/<int:user_id>/', views.user_profile, name='user_profile'),

    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('all_courses/', views.all_courses, name='all_courses'),
    path('enroll_course/<int:course_id>/', views.enroll_course, name='enroll_course'),
    path('leave_course/<int:course_id>/', views.leave_course, name='leave_course'),
    path('course_content/<int:course_id>/', views.course_content, name='course_content'),

    path('api/', include('elearningapp.api')),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

