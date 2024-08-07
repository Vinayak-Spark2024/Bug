# project/models.py
from django.db import models
from department.models import Department
from accounts.models import CustomUser

class Project(models.Model):
    project_name = models.CharField(max_length=255)
    project_description = models.TextField()
    project_duration = models.IntegerField(help_text="Duration in days")
    client_name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, related_name='projects', on_delete=models.CASCADE)
    submission_date = models.DateField()
    updated_date = models.DateField(auto_now=True)    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='projects')  # Added field



    def __str__(self):
        return f"{self.project_name} - {self.department.department} - {self.user.username} - {self.department.role}"
