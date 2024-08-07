from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import Department
from .serializers import DepartmentSerializer
from rest_framework.exceptions import PermissionDenied

class DepartmentListCreateView(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class DepartmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

