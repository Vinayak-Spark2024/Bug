from rest_framework.permissions import BasePermission

class IsAdminOrManagerOrTeamLead(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user and user.is_authenticated:
            if user.is_staff:
                return True
            if user.role in ['manager', 'team_lead']:
                return True
            if view.kwargs.get('pk') == str(user.id):
                return True
        return False
    
"""class IsAdminOrManagerOrTeamLead(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user and user.is_authenticated:
            if user.is_staff:
                return True
            if user.role in ['manager', 'team_lead']:
                return True
        return False"""