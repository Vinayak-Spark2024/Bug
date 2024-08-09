# views.py for bug app (updated)

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from .models import Bug
from .serializers import BugSerializer




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
    
    def delete(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

class BugStatusUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk, format=None):
        try:
            bug = Bug.objects.get(pk=pk)
        except Bug.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if bug.created_by != request.user and not request.user.is_superuser:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = BugSerializer(bug, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)