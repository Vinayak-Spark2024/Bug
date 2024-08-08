from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Department(models.Model):
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

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    dept = models.CharField(max_length=20, choices=DEPT_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role} - {self.dept}"