# bug/models.py
from django.db import models
from accounts.models import CustomUser
from django.contrib.auth import get_user_model
from project.models import Project 
from department.models import Department

User = get_user_model()

class Bug(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    SEVERITY_CHOICES = [
        ('critical', 'Critical'),
        ('major', 'Major'),
        ('normal', 'Normal'),
        ('minor', 'Minor'),
        ('trivial', 'Trivial'),
        ('enhancement', 'Enhancements/Feature Requests'),
    ]

    TYPE_CHOICES = [
        ('error', 'Error'),
        ('mistake', 'Mistake'),
        ('bug', 'Bug'),
        ('issue', 'Issue'),
        ('fault', 'Fault'),
        ('defect', 'Defect'),
    ]

    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('in_progress', 'In Progress'),
    ]

    bug_name = models.CharField(max_length=255)
    project = models.ForeignKey(Project, related_name='created_bugs', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/', verbose_name='Bug_Image')
    department = models.ForeignKey(Department, related_name='created_bugs', on_delete=models.CASCADE)
    bug_date = models.DateField()
    bug_priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    bug_severity = models.CharField(max_length=15, choices=SEVERITY_CHOICES)
    bug_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    created_by = models.ForeignKey(CustomUser, related_name='created_bugs', on_delete=models.CASCADE)
    description = models.TextField()
    updated_time = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)
    is_current_project = models.BooleanField(default=True)

    def __str__(self):
        return self.bug_name
    
    def delete(self, *args, **kwargs):
        raise NotImplementedError("Deleting bugs is not allowed. Set the status to 'closed' instead.")
