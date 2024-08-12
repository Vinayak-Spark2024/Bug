# serializers.py for bug app (updated)

from rest_framework import serializers
from .models import Bug
from django.contrib.auth import get_user_model


class BugSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')
    assigned_to = serializers.SlugRelatedField(slug_field='username', queryset=get_user_model().objects.all(), required=False)

    class Meta:
        model = Bug
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if hasattr(self, 'initial_data'):
            project_id = self.initial_data.get('project_id')

    """def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        project_id = self.initial_data.get('project_id')
        if project_id:
            self.fields['assigned_to'].queryset = get_user_model().objects.filter(
                id__in=ProjectUser.objects.filter(project_id=project_id).values_list('user_id', flat=True)
            )"""
