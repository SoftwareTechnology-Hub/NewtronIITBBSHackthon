# elearnapp/models.py
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('faculty', 'Faculty'),
        ('admin', 'Admin'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return self.username
    groups = models.ManyToManyField(Group, related_name="customuser_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions", blank=True)
class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    faculty = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'faculty'})
    students = models.ManyToManyField(CustomUser, related_name='enrolled_courses', limit_choices_to={'role': 'student'})
    start_date = models.DateField(null=True, blank=True)  # Allow null values for existing data
    image = models.ImageField(upload_to='course_images/', null=True, blank=True)  # New field

    def __str__(self):
        return self.title

from django.db import models

class Lecture(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lectures")
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True, null=True)
    pdf_file = models.FileField(upload_to="pdfs/", blank=True, null=True)
    video_file = models.FileField(upload_to="videos/", blank=True, null=True)
    created_at = models.DateField(null=True, blank=True)  # Step 1: Allow null values temporarily

    def __str__(self):
        return f"{self.course.title} - {self.title} ({self.created_at})"
class Enrollment(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_on = models.DateTimeField(auto_now_add=True)
class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    deadline = models.DateTimeField()

class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    file = models.FileField(upload_to='submissions/')
    submitted_on = models.DateTimeField(auto_now_add=True)
    grade = models.FloatField(null=True, blank=True)
    feedback = models.TextField(blank=True)
from django.db import models
from django.utils import timezone

class Announcement(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
class Notification(models.Model):
    faculty = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'faculty'})
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
    
from django.db import models
from django.conf import settings  # Ensure we use the correct user model reference

from django.db import models
from django.conf import settings

from django.db import models
from django.conf import settings

class Quiz(models.Model):
    faculty = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    time_limit = models.IntegerField()  # in minutes
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.TextField()
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    correct_option = models.IntegerField(default=0)  # 0 to 3

    def __str__(self):
        return self.text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class StudentResponse(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)  # Make sure this model exists
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE)  # Ensure Choice exists
    is_correct = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.is_correct = self.selected_choice.is_correct
        super().save(*args, **kwargs)
