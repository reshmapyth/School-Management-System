from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken,Token
from accounts. models import *
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from . serializers import *
import os
import hashlib


class CommonloginView(APIView):
    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            refresh = RefreshToken.for_user(user)


            if user.is_superuser :
                role="Admin"
                response_data = {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "role": role,
                    "email": user.email,
                    "full_name": user.full_name,
                }
                return Response(response_data,status=status.HTTP_200_OK)
            elif user.is_office_staff:
                role="Office Staff"
                response_data = {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "role": role,
                    "email": user.email,
                    "full_name": user.full_name,
                }
                return Response(response_data,status=status.HTTP_200_OK)
            elif user.is_librarian:
                role="Librarian"
                response_data = {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "role": role,
                    "email": user.email,
                    "full_name": user.full_name,
                }
                return Response(response_data,status=status.HTTP_200_OK)