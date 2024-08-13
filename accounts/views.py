from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from .permissions import IsAdminOrManagerOrTeamLead
from .serializers import RegisterSerializer, LoginSerializer, UserProfileSerializer, AdminUserProfileSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAdminOrManagerOrTeamLead]
    serializer_class = RegisterSerializer

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token is None:
                return Response({'detail': 'Refresh token is required.'}, status=status.HTTP_400_BAD_REQUEST)

            # Validate and blacklist the refresh token
            token = RefreshToken(refresh_token)
            try:
                outstanding_token = OutstandingToken.objects.get(token=token)
            except OutstandingToken.DoesNotExist:
                return Response({'detail': 'Invalid refresh token.'}, status=status.HTTP_400_BAD_REQUEST)

            BlacklistedToken.objects.create(token=outstanding_token)
            
            return Response({'detail': 'Logged out successfully.'}, status=status.HTTP_205_RESET_CONTENT)
        
        except TokenError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.user.is_staff or self.request.user.role in ['manager', 'team_lead']:
            return AdminUserProfileSerializer
        return UserProfileSerializer

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.role in ['manager', 'team_lead']:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

    def get_object(self):
        obj = super().get_object()
        # Ensure that regular users can only access their own profile
        if not (self.request.user.is_staff or self.request.user.role in ['manager', 'team_lead']) and obj.id != self.request.user.id:
            self.permission_denied(self.request, message="You do not have permission to access this profile.")
        return obj
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = AdminUserProfileSerializer
    permission_classes = [IsAuthenticated, IsAdminOrManagerOrTeamLead]
