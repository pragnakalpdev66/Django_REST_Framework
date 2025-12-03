from django.db import models
from django.contrib.auth.models import AbstractUser
# inbuilt user model but customize
# 1st sprint Rolebased Authentication 


class User(AbstractUser):
    STUDENT = 'student'
    INSTRUCTOR = 'instructor'

    ROLE_CHOICES = (
        (STUDENT, 'Student'),
        (INSTRUCTOR, 'Instructor'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} ({self.role})"
