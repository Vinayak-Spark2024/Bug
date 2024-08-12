from rest_framework.permissions import BasePermission

class IsAdminOrManagerOrTeamLead(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user and user.is_authenticated:
            # Allow access if the user is an admin
            if user.is_staff:
                return True
            # Allow access if the user is a manager or team lead
            if user.role in ['manager', 'team_lead']:
                return True
        return False
