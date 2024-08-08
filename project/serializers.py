from rest_framework import serializers
from .models import Project, ProjectUser

class ProjectUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectUser
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    projectuser_set = ProjectUserSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'
