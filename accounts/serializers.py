from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role', 'dept']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role'],
            dept=validated_data['dept']
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(read_only=True)
    user_id = serializers.IntegerField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        user = authenticate(username=email, password=password)
        if user is None:
            raise serializers.ValidationError('Invalid login credentials')

        refresh = RefreshToken.for_user(user)
        data = {
            'user_id': user.id,
            'username': user.username,
            'is_staff': user.is_staff,
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }
        return data

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'dept', 'is_staff']
        extra_kwargs = {'password': {'write_only': True}}

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class UserAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'dept', 'is_staff']
        extra_kwargs = {'password': {'write_only': True}}

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
    

