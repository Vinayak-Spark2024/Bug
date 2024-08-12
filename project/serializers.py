from rest_framework import serializers
from .models import Project
from accounts.models import CustomUser

class ProjectSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), many=True)

    class Meta:
        model = Project
        fields = '__all__'
