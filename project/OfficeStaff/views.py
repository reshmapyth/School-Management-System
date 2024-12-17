from django.shortcuts import render
from rest_framework import serializers
from rest_framework import generics, permissions,status,filters
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
from rest_framework.response import Response
from accounts.models import *
from rest_framework.authentication import TokenAuthentication


# Create your views here.
class AdminLoginView(generics.GenericAPIView):
    serializer_class = OfficeStaffLoginSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = OfficeStaffLoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'Admin Login successful',
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_id': user.id,
            'email': user.email
        }, status=status.HTTP_200_OK)
