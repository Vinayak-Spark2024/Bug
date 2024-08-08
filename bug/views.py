# views.py for bug app (updated)

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.utils import timezone
from .models import Bug
from .serializers import BugSerializer
from project.models import ProjectUser

class BugListCreateView(generics.ListCreateAPIView):
    serializer_class = BugSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return Bug.objects.all()
        return Bug.objects.filter(created_by=user) | Bug.objects.filter(assigned_to=user)

class BugDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = BugSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return Bug.objects.all()
        return Bug.objects.filter(created_by=user) | Bug.objects.filter(assigned_to=user)

class BugStatusUpdateView(generics.UpdateAPIView):
    serializer_class = BugSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return Bug.objects.all()
        return Bug.objects.filter(created_by=user) | Bug.objects.filter(assigned_to=user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data
        if 'status' in data:
            instance.status = data['status']
            instance.updated_date = timezone.now()
            instance.save()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)