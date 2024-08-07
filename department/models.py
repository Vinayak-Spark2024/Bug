# department/models.py
from django.db import models
from django.conf import settings
from accounts.models import CustomUser

class Department(models.Model):
    CUSTOMER = 'Customer'
    DEVOPS = 'DevOps'
    JAVA = 'Java' 
    MANAGEMENT = 'Management'
    PHP = 'PHP'
    PYTHON = 'Python'

    DEPARTMENT_CHOICES = [
        (CUSTOMER, 'Customer'),
        (DEVOPS, 'DevOps'),
        (JAVA, 'Java'),       
        (MANAGEMENT, 'Management'),
        (PHP, 'PHP'),
        (PYTHON, 'Python')
    ]

    PROJECT_LEAD = 'Project Lead'
    DEVELOPER = 'Developer'
    TESTER = 'Tester'
    MANAGER = 'Manager'
    CLIENT = 'Client'
    
    ROLE_CHOICES = [
        (PROJECT_LEAD, 'Project Lead'),
        (DEVELOPER, 'Developer'),
        (TESTER, 'Tester'),
        (MANAGER, 'Manager'),
        (CLIENT, 'Client')
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.department} - {self.role}"