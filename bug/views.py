# bug/views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Bug
from .serializers import BugSerializer

class BugListCreateView(generics.ListCreateAPIView):
    queryset = Bug.objects.all()
    serializer_class = BugSerializer
    permission_classes = (IsAuthenticated,)

class BugDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bug.objects.all()
    serializer_class = BugSerializer
    permission_classes = (IsAuthenticated,)