from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Course, Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    real_name = forms.CharField(required=True, max_length=100, help_text='Enter your real name')
    is_teacher = forms.BooleanField(required=False, help_text='Check if you are registering as a teacher.')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'real_name', 'is_teacher']

class CourseCreationForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'materials'] 

class TeacherProfileForm(forms.ModelForm):
    username = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    # Define other fields as before
    class Meta:
        model = Profile
        fields = ['username', 'email', 'real_name', 'photo', 'status']
    def __init__(self, *args, **kwargs):
        super(TeacherProfileForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['username'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email
    def save(self, commit=True):
        profile = super(TeacherProfileForm, self).save(commit=False)
        if commit:
            user = profile.user
            user.username = self.cleaned_data.get('username', user.username)
            user.email = self.cleaned_data.get('email', user.email)
            user.save()
            profile.save()
        return profile