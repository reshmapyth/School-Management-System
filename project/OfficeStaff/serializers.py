from rest_framework import serializers
from accounts.models import *
from django.contrib.auth import authenticate

class OfficeStaffLoginSerializer(serializers.Serializer):
   
    email = serializers.EmailField(required=True, help_text="Enter your username address.")
    password = serializers.CharField(required=True, help_text="Enter your password.")

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if user is None or not user.is_staff:
                raise serializers.ValidationError("Invalid email or password.")
        else:
            raise serializers.ValidationError("Email and password are required.")

        attrs['user'] = user
        return attrs
    