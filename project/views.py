from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Project, ProjectUser
from .serializers import ProjectSerializer, ProjectUserSerializer
from rest_framework.permissions import IsAuthenticated

class ProjectListCreateView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

class ProjectUserCreateView(generics.CreateAPIView):
    queryset = ProjectUser.objects.all()
    serializer_class = ProjectUserSerializer
    permission_classes = [permissions.IsAdminUser]

class UpdateProjectStatusView(generics.UpdateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data

        instance.submission_date = data.get("submission_date", instance.submission_date)
        instance.updated_date = data.get("updated_date", instance.updated_date)
        instance.status = data.get("status", instance.status)

        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)
