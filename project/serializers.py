# project/serializers.py
from rest_framework import serializers
from .models import Project
from department.models import Department

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'project_name', 'project_description', 'project_duration', 'client_name', 'department', 'submission_date', 'updated_date', 'user']
        read_only_fields = ['department', 'user']

    def create(self, validated_data):
        user = self.context['request'].user
        department = Department.objects.filter(user=user).first()  # Assuming a user can belong to only one department

        project = Project(
            project_name=validated_data['project_name'],
            project_description=validated_data['project_description'],
            project_duration=validated_data['project_duration'],
            client_name=validated_data['client_name'],
            department=department,
            submission_date=validated_data['submission_date'],
            user=user
        )
        project.save()
        return project

    def update(self, instance, validated_data):
        instance.project_name = validated_data.get('project_name', instance.project_name)
        instance.project_description = validated_data.get('project_description', instance.project_description)
        instance.project_duration = validated_data.get('project_duration', instance.project_duration)
        instance.client_name = validated_data.get('client_name', instance.client_name)
        instance.submission_date = validated_data.get('submission_date', instance.submission_date)
        instance.save()
        return instance