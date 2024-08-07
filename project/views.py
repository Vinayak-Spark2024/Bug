from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Project
from .serializers import ProjectSerializer
from department.models import Department

class ProjectListCreateView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def perform_create(self, serializer):
        user = self.request.user
        department = Department.objects.filter(user=user).first()  # Assuming a user can belong to only one department
        serializer.save(user=user, department=department)

class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
