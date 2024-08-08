from django.urls import path
from .views import ProjectListCreateView, ProjectDetailView, ProjectUserCreateView, UpdateProjectStatusView

urlpatterns = [
    path('projects/', ProjectListCreateView.as_view(), name='project-list-create'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('projects/assign/', ProjectUserCreateView.as_view(), name='project-user-assign'),
    path('projects/<int:pk>/update-status/', UpdateProjectStatusView.as_view(), name='update-project-status'),
]
