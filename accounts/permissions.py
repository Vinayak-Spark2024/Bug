from rest_framework.permissions import BasePermission

class IsAdminOrManagerOrTeamLead(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user and user.is_authenticated:
            if user.is_staff:
                return True
            if user.role in ['manager', 'team_lead']:
                return True
        return False

class IsAdminOrManager(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        # Allow access to admin and manager for GET, POST (e.g., listing users or creating a user)
        if request.method in ['GET', 'POST']:
            return user.is_staff or user.role in ['manager']
        # Allow access to admin and manager for PUT, PATCH, DELETE (e.g., updating or deleting a user)
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return user.is_staff or user.role in ['manager']
        return False

    def has_object_permission(self, request, view, obj):
        user = request.user
        # Admins and Managers can perform any action on users
        if user.is_staff or user.role in ['manager']:
            return True
        return False


class IsOwnProfile(BasePermission):

    def has_permission(self, request, view):
        # Allow authenticated users to view their own profile
        if request.method in ['GET', 'PUT', 'PATCH']:
            return request.user and request.user.is_authenticated
        return False

    def has_object_permission(self, request, view, obj):
        # Allow users to access or modify their own profile
        return obj == request.user