from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    Register a new user.
    
    This endpoint allows anyone to create a new account.
    It returns user information and JWT tokens upon successful registration.
    """
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        # Generate JWT tokens for the new user
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        
        # Return user info and tokens
        user_serializer = UserSerializer(user)
        return Response({
            'message': 'User registered successfully',
            'user': user_serializer.data,
            'tokens': {
                'access': str(access),
                'refresh': str(refresh)
            }
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    Login a user.
    
    This endpoint authenticates a user with username/password
    and returns JWT tokens upon successful login.
    """
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        
        # Return user info and tokens
        user_serializer = UserSerializer(user)
        return Response({
            'message': 'Login successful',
            'user': user_serializer.data,
            'tokens': {
                'access': str(access),
                'refresh': str(refresh)
            }
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
