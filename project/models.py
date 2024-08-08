from django.db import models
from django.contrib.auth import get_user_model
from department.models import Department

User = get_user_model()

class Project(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('in_progress', 'In Progress')
    ]

    project_name = models.CharField(max_length=255)
    project_duration = models.IntegerField()  # Duration in days
    client_name = models.CharField(max_length=255)
    submission_date = models.DateField()
    updated_date = models.DateField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    users = models.ManyToManyField(User, through='ProjectUser')
    
    def __str__(self):
        return self.project_name

class ProjectUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.CharField(max_length=20)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.project.project_name} - {self.role}"
