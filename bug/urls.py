# bug/urls.py
from django.urls import path
from .views import BugListCreateView, BugDetailView

urlpatterns = [
    path('bugs/', BugListCreateView.as_view(), name='bug-list-create'),
    path('bugs/<int:pk>/', BugDetailView.as_view(), name='bug-detail'),
]
