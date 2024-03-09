from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    real_name = models.CharField(max_length=100, null=True, blank=True)
    is_teacher = models.BooleanField(default=False)
    photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)  
    status = models.CharField(max_length=200, null=True, blank=True)  
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    teacher = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='courses_taught')
    materials = models.FileField(upload_to='course_materials/', null=True, blank=True)

    def __str__(self):
        return self.title

class Enrollment(models.Model):
    student = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrolled_students')
    date_enrolled = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username} enrolled in {self.course.title}"

class Feedback(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='feedbacks')
    student = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='given_feedbacks')
    text = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return f"Feedback by {self.student.user.username} for {self.course.title}"

class StatusUpdate(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='status_updates')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Status update by {self.user.user.username}"
