from rest_framework.response import Response
from .serializers import *
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from accounts.models import User, District, State, Country_Codes
from rest_framework import filters
from django.utils.timezone import now

#Librarian Register

class LibrarianRegister(generics.GenericAPIView):
    serializer_class = LibrarinSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_superuser == False:
            return Response({"error": "Not Logged in as Admin"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)  # Log validated data for debugging

        email = serializer.validated_data.get('email') 
        phone_number = serializer.validated_data.get('phone_number')

        # Check if librarian already exists with the same email
        if User.objects.filter(email=email).exists():
            return Response({"error": f"Librarian already exists with the email: {email}"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if librarian already exists with the same phone number
        if User.objects.filter(phone_number=phone_number).exists():
            return Response({"error": f"Librarian already exists with the phone number: {phone_number}"}, status=status.HTTP_400_BAD_REQUEST)

        password = serializer.validated_data.get('password')
        
        # Create new user instance
        user = User.objects.create(
            email=email,
            full_name=serializer.validated_data.get('full_name'),
            address=serializer.validated_data.get('address'),
            place=serializer.validated_data.get('place'),
            pin_code=serializer.validated_data.get('pin_code'),
            district=serializer.validated_data.get('district'),
            state=serializer.validated_data.get('state'),
            phone_number=serializer.validated_data.get('phone_number'),
            country_code=serializer.validated_data.get('country_code'),
            is_librarian=True
        )
        
        # Set password and save the user
        user.set_password(password)
        user.save()

        # Create Librarian profile
        librarian = Librarian.objects.create(
            user=user,
            book_name=serializer.validated_data.get('book_name'),
            created_date=serializer.validated_data.get('created_date', now())
        )

        return Response({"message": "Librarian created successfully", "librarian_id": librarian.custom_id})




class LibrarianData(generics.ListCreateAPIView):
    serializer_class = LibrarianDataserializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.is_superuser:
            return Librarian.objects.none()

        queryset = Librarian.objects.all()
        print(queryset)  # Debugging line to see the queryset
        return queryset
    def list(self, request, *args, **kwargs):
        # Custom response to check the data
        response = super().list(request, *args, **kwargs)
        print(response.data)  # Print serialized data to the console
        return response
    

# class LibrarianUpdate(generics.ListCreateAPIView):
#     serializer_class = LibrarianUpdateSerializer
#     permission_classes = [IsAuthenticated]

#     def patch(self, request, *args, **kwargs):
#         user = self.request.user
#         if User.objects.filter(email=user,is_superuser=False).exists():
#             return Response({"error": "not admin login"}, status=status.HTTP_205_RESET_CONTENT)
#         data =self.request.data
#         if data :
#             if Librarian.objects.filter(custom_id=data['id']).exists():
#                 obj = Librarian.objects.get(custom_id=data['id'])
#                 user_serializer=UserSerializer(user,data=data,partial=True )
#                 user_serializer.is_valid(raise_exception=True)
#                 user_serializer.save()
#                 serializer = Librarianviewserializer(obj,data=data,partial=True)
#                 serializer.is_valid(raise_exception=True)
#                 serializer.save()
#                 return Response({"msg":data['id']+"updated","data":serializer.data})
#             else:
#                 return Response({"error":" data is in id"},status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response({"error":"id or data not updated"},status=status.HTTP_400_BAD_REQUEST)


# class LibrarianDelete(generics.ListCreateAPIView):
#     serializer_class = Librarianviewserializer
#     permission_classes = [IsAuthenticated]

#     def delete(self, request, *args, **kwargs):
#         user = self.request.user
#         if User.objects.filter(email=user,is_superuser=False).exists():
#             return Response({"error": "not admin login"}, status=status.HTTP_205_RESET_CONTENT)
#         data =self.request.data
#         if data :
#             if Librarian.objects.filter(custom_id=data['id']).exists():
#                 obj = Librarian.objects.get(custom_id=data['id'])
#                 obj.delete()
#                 return Response({"msg":data['id']+"deleted"})
#             else:
#                 return Response({"error":"no librarian inthis id"},status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response({"error":"pass id is deleted"},status=status.HTTP_400_BAD_REQUEST)


class LibrarianUpdate(generics.ListCreateAPIView):
    serializer_class = Librarianviewserializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_superuser:
            return Response({"error": "Not logged in as admin"}, status=status.HTTP_403_FORBIDDEN)

        data = self.request.data

        # Check if 'id' exists in the request data
        if 'id' not in data:
            return Response({"error": "'id' field is required"}, status=status.HTTP_400_BAD_REQUEST)

        librarian_id = data['id']

        try:
            # Fetch the librarian object
            librarian = Librarian.objects.get(custom_id=librarian_id)
        except Librarian.DoesNotExist:
            return Response({"error": f"Librarian with custom_id {librarian_id} does not exist"}, status=status.HTTP_404_NOT_FOUND)

        # Proceed with the update
        user_serializer = UserSerializer(librarian.user, data=data, partial=True)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()

        serializer = Librarianviewserializer(librarian, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"msg": f"{librarian_id} updated", "data": serializer.data})

class LibrarianDelete(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_superuser:
            return Response({"error": "Not logged in as admin"}, status=status.HTTP_403_FORBIDDEN)

        data = request.data
        if 'id' not in data:
            return Response({"error": "ID is required to delete librarian"}, status=status.HTTP_400_BAD_REQUEST)
        


from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import OfficeStaffSerializer 
from django.utils.timezone import now


class OfficeStaffRegister(generics.GenericAPIView):
    serializer_class = OfficeStaffSerializer  # Adjust to your OfficeStaff serializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_superuser:
            return Response({"error": "Not Logged in as Admin"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)  # Log validated data for debugging

        email = serializer.validated_data.get('email')
        phone_number = serializer.validated_data.get('phone_number')

        # Check if office staff already exists with the same email
        if User.objects.filter(email=email).exists():
            return Response({"error": f"Office staff already exists with the email: {email}"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if office staff already exists with the same phone number
        if User.objects.filter(phone_number=phone_number).exists():
            return Response({"error": f"Office staff already exists with the phone number: {phone_number}"}, status=status.HTTP_400_BAD_REQUEST)

        password = serializer.validated_data.get('password')
        
        # Create new user instance for Office Staff
        user = User.objects.create(
            email=email,
            full_name=serializer.validated_data.get('full_name'),
            address=serializer.validated_data.get('address'),
            place=serializer.validated_data.get('place'),
            pin_code=serializer.validated_data.get('pin_code'),
            district=serializer.validated_data.get('district'),
            state=serializer.validated_data.get('state'),
            phone_number=serializer.validated_data.get('phone_number'),
            country_code=serializer.validated_data.get('country_code'),
            is_office_staff=True
        )
        
        # Set password and save the user
        user.set_password(password)
        user.save()

        # Create OfficeStaff profile
        office_staff = OfficeStaff.objects.create(
            user=user,
            phone_number=serializer.validated_data.get('phone_number'),
            address=serializer.validated_data.get('address'),
            created_date=serializer.validated_data.get('created_date', now())
        )

        return Response({"message": "Office Staff created successfully", "office_staff_id": office_staff.id})
    
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import OfficeStaffSerializer
from django.shortcuts import get_object_or_404


# Create Office Staff (Already done in OfficeStaffRegister)
class OfficeStaffCreateView(generics.GenericAPIView):
    serializer_class = OfficeStaffSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_superuser:
            return Response({"error": "Not Logged in as Admin"}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        phone_number = serializer.validated_data.get('phone_number')

        # Validation
        if User.objects.filter(email=email).exists():
            return Response({"error": f"Office staff already exists with the email: {email}"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(phone_number=phone_number).exists():
            return Response({"error": f"Office staff already exists with the phone number: {phone_number}"}, status=status.HTTP_400_BAD_REQUEST)

        # Create User and Office Staff
        user = User.objects.create(
            email=email,
            full_name=serializer.validated_data.get('full_name'),
            address=serializer.validated_data.get('address'),
            place=serializer.validated_data.get('place'),
            pin_code=serializer.validated_data.get('pin_code'),
            district=serializer.validated_data.get('district'),
            state=serializer.validated_data.get('state'),
            phone_number=phone_number,
            country_code=serializer.validated_data.get('country_code'),
            is_office_staff=True
        )
        user.set_password(serializer.validated_data.get('password'))
        user.save()

        office_staff = OfficeStaff.objects.create(
            user=user,
            phone_number=phone_number,
            address=serializer.validated_data.get('address'),
        )

        return Response({"message": "Office Staff created successfully", "office_staff_id": office_staff.id})


# Read/Retrieve Office Staff
class OfficeStaffRetrieveView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OfficeStaffSerializer

    def get(self, request, pk, *args, **kwargs):
        user = self.request.user
        if not user.is_superuser:
            return Response({"error": "Not Logged in as Admin"}, status=status.HTTP_403_FORBIDDEN)

        office_staff = get_object_or_404(OfficeStaff, pk=pk)
        serializer = self.get_serializer(office_staff)
        return Response(serializer.data)


# Update Office Staff
class OfficeStaffUpdateView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OfficeStaffSerializer

    def put(self, request, pk, *args, **kwargs):
        user = self.request.user
        if not user.is_superuser:
            return Response({"error": "Not Logged in as Admin"}, status=status.HTTP_403_FORBIDDEN)

        office_staff = get_object_or_404(OfficeStaff, pk=pk)
        serializer = self.get_serializer(office_staff, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Office Staff updated successfully", "data": serializer.data})


# Delete Office Staff
class OfficeStaffDeleteView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk, *args, **kwargs):
        user = self.request.user
        if not user.is_superuser:
            return Response({"error": "Not Logged in as Admin"}, status=status.HTTP_403_FORBIDDEN)

        office_staff = get_object_or_404(OfficeStaff, pk=pk)
        office_staff.delete()
        return Response({"message": "Office Staff deleted successfully"})
    

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import StudentSerializer 
from django.utils.timezone import now


class StudentRegister(generics.GenericAPIView):
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_superuser:
            return Response({"error": "Not Logged in as Admin"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)  # Log validated data for debugging

        email = serializer.validated_data.get('email')
        phone_number = serializer.validated_data.get('phone_number')

        # Check if student already exists with the same email
        if User.objects.filter(email=email).exists():
            return Response({"error": f"Student already exists with the email: {email}"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if student already exists with the same phone number
        if User.objects.filter(phone_number=phone_number).exists():
            return Response({"error": f"Student already exists with the phone number: {phone_number}"}, status=status.HTTP_400_BAD_REQUEST)

        password = serializer.validated_data.get('password')
        
        # Create new user instance for Student
        user = User.objects.create(
            email=email,
            full_name=serializer.validated_data.get('full_name'),
            address=serializer.validated_data.get('address'),
            phone_number=serializer.validated_data.get('phone_number'),
            country_code=serializer.validated_data.get('country_code'),
            is_student=True  # Assuming you have an `is_student` field in your User model
        )
        
        # Set password and save the user
        user.set_password(password)
        user.save()

        # Create Student profile
        student = Student.objects.create(
            user=user,
            first_name=serializer.validated_data.get('first_name'),
            last_name=serializer.validated_data.get('last_name'),
            class_name=serializer.validated_data.get('class_name'),
            created_date=serializer.validated_data.get('created_date', now())
        )

        return Response({"message": "Student created successfully", "student_id": student.id})
    
class StudentDetailView(generics.RetrieveAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]


# Update Student Details
class StudentUpdateView(generics.UpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_superuser:
            return Response({"error": "Not Logged in as Admin"}, status=status.HTTP_403_FORBIDDEN)

        return super().patch(request, *args, **kwargs)


# Delete Student
class StudentDeleteView(generics.DestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_superuser:
            return Response({"error": "Not Logged in as Admin"}, status=status.HTTP_403_FORBIDDEN)

        return super().delete(request, *args, **kwargs)


# List All Students
class StudentListView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

from rest_framework.views import APIView

# Library History View
class LibraryHistoryView(APIView):
    def get(self, request, *args, **kwargs):
        histories = LibraryHistory.objects.all()
        serializer = LibraryHistorySerializer(histories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Fees History View
class FeesHistoryView(APIView):
    def get(self, request, *args, **kwargs):
        fees = FeesRemarks.objects.all()
        serializer = FeesRemarksSerializer(fees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



