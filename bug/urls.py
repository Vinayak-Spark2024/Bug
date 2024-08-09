# urls.py for bug app

from django.urls import path
from .views import BugListCreateView, BugDetailView, BugStatusUpdateView

urlpatterns = [
    path('bugs/', BugListCreateView.as_view(), name='bug-list-create'),
    path('bugs/<int:pk>/', BugDetailView.as_view(), name='bug-detail'),
    path('bugs/<int:pk>/status/', BugStatusUpdateView.as_view(), name='bug-status-update'),
]