from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    DEPT_CHOICES = [
        ('python', 'Python'),
        ('php', 'PHP'),
        ('java', 'Java'),
        ('angular', 'Angular'),
        ('mobile_app', 'Mobile App'),
        ('devops', 'DevOps'),
        ('tester', 'Tester'),
        ('management', 'Management'),
        ('client', 'Client')
    ]

    ROLE_CHOICES = [
        ('team_lead', 'Team Lead'),
        ('developer', 'Developer'),
        ('customer', 'Customer'),
        ('tester', 'Tester'),
        ('manager', 'Manager')
    ]
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    dept = models.CharField(max_length=20, choices=DEPT_CHOICES)
    is_staff = models.BooleanField(default=False)

    def __str__(self):
        return self.username
