from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .forms import UserRegisterForm
from .forms import CourseCreationForm, TeacherProfileForm
from .models import Profile, Course, Enrollment
from rest_framework import viewsets
from .serializers import CourseSerializer

def home(request):
    return render(request, 'elearningapp/home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            real_name = form.cleaned_data.get('real_name')
            is_teacher = form.cleaned_data.get('is_teacher')
            # Assume Profile model includes real_name and is_teacher fields
            Profile.objects.update_or_create(user=user, defaults={'real_name': real_name, 'is_teacher': is_teacher})
            messages.success(request, f'Account created for {user.username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'elearningapp/register.html', {'form': form})

@login_required
def dashboard_redirect(request):
    if hasattr(request.user, 'profile'):
        if request.user.profile.is_teacher:
            return redirect('teacher_dashboard')
        else:
            return redirect('student_dashboard')
    return redirect('home')


@login_required
def teacher_dashboard(request):
    if not hasattr(request.user, 'profile') or not request.user.profile.is_teacher:
        return redirect('home')  # Or some error message/page
    
    courses = Course.objects.filter(teacher=request.user.profile).annotate(
        enrolled_students_count=Count('enrolled_students')
    )
    
    return render(request, 'elearningapp/teacher_dashboard.html', {'courses': courses})



@login_required
def student_dashboard(request):
    # Assuming Profile has a user field linking to the Django user
    user_profile = request.user.profile
    enrolled_courses = Course.objects.filter(enrolled_students__student=user_profile)
    context = {
        'enrolled_courses': enrolled_courses,
        'upcoming_deadlines': [],  # Add your logic for upcoming deadlines
    }
    return render(request, 'elearningapp/student_dashboard.html', context)

@login_required
def create_course(request):
    if request.method == 'POST':
        form = CourseCreationForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user.profile  # Set the course's teacher
            course.save()
            # Redirect to a new URL:
            return redirect('teacher_dashboard')  # Redirect to the teacher dashboard or another appropriate page
    else:
        form = CourseCreationForm()  # An unbound form
    
    return render(request, 'elearningapp/teacher_create-course.html', {'form': form})

@login_required
def edit_course(request, course_id):
    course = Course.objects.get(id=course_id)
    if request.method == 'POST':
        form = CourseCreationForm (request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated successfully!')
            return redirect('teacher_dashboard')
    else:
        form = CourseCreationForm (instance=course)
    return render(request, 'elearningapp/teacher_edit-course.html', {'form': form})


@login_required
def delete_course(request, course_id):
    if not request.user.profile.is_teacher:
        # Redirect the user if they are not a teacher or not authorized
        return redirect('home')
    try:
        course = Course.objects.get(id=course_id, teacher=request.user.profile)
        course.delete()
        messages.success(request, "Course deleted successfully.")
    except Course.DoesNotExist:
        messages.error(request, "Course not found.")
    return redirect('teacher_dashboard')

@login_required
def edit_teacher_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = TeacherProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # Save Profile form
            profile_form = form.save(commit=False)
            profile_form.user.username = form.cleaned_data['username']
            profile_form.user.email = form.cleaned_data['email']
            # Consider handling password change here
            profile_form.user.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('teacher_dashboard')
    else:
        form = TeacherProfileForm(instance=profile)
    return render(request, 'elearningapp/teacher_private-profile.html', {'form': form})

@login_required
def search_users(request):
    user_type = request.GET.get('type')
    profiles = Profile.objects.all()
    if user_type == 'student':
        profiles = profiles.filter(is_teacher=False)
    elif user_type == 'teacher':
        profiles = profiles.filter(is_teacher=True)
    return render(request, 'elearningapp/teacher_user-search.html', {'profiles': profiles})

@login_required
def user_profile(request, user_id):
    profile = get_object_or_404(Profile, user__id=user_id)
    courses = []
    if profile.is_teacher:
        courses = Course.objects.filter(teacher=profile)
    else:
        enrollments = Enrollment.objects.filter(student=profile)
        courses = [enrollment.course for enrollment in enrollments]

    return render(request, 'elearningapp/teacher_user-search_user-profile.html', {'profile': profile, 'courses': courses})

@login_required
def all_courses(request):
    courses = Course.objects.all()
    enrolled_courses = Enrollment.objects.filter(student=request.user.profile).values_list('course_id', flat=True)
    context = {
        'courses': courses,
        'enrolled_course_ids': list(enrolled_courses),
    }
    return render(request, 'elearningapp/student_courses.html', context)

@login_required
def enroll_course(request, course_id):
    if request.method == 'POST':
        course = Course.objects.get(id=course_id)
        Enrollment.objects.get_or_create(student=request.user.profile, course=course)
        messages.success(request, 'Successfully enrolled in the course!')
    return redirect('all_courses')

@login_required
def leave_course(request, course_id):
    if request.method == 'POST':
        course = Course.objects.get(id=course_id)
        enrollment = Enrollment.objects.filter(student=request.user.profile, course=course)
        if enrollment.exists():
            enrollment.delete()
            messages.success(request, 'You have left the course.')
    return redirect('all_courses')

@login_required
def course_content(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'elearningapp/course_content.html', {'course': course})

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer