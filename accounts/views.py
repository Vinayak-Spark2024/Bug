from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from .permissions import IsAdminOrManagerOrTeamLead, IsAdminOrManager, IsOwnProfile
from .serializers import RegisterSerializer, LoginSerializer, UserProfileSerializer, UserAdminSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsAdminOrManagerOrTeamLead]
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

class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserAdminSerializer
    permission_classes = [IsAdminOrManager]

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserAdminSerializer
    permission_classes = [IsAdminOrManager]

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsOwnProfile]

    def get_object(self):
        return self.request.user