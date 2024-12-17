from rest_framework import serializers
from accounts.models import *


class LibrarinSerializer(serializers.Serializer):

# user
    email = serializers.EmailField(source='user.email')
    password = serializers.CharField(required=True)
    full_name = serializers.CharField(required=True)
    address = serializers.CharField(required=True)
    place = serializers.CharField(required=True)
    pin_code = serializers.CharField(required=True)
    district = serializers.PrimaryKeyRelatedField(queryset=District.objects.all())
    state =serializers.PrimaryKeyRelatedField(queryset=State.objects.all())
    phone_number = serializers.CharField(required=True)
    country_code =serializers.PrimaryKeyRelatedField(queryset=Country_Codes.objects.all())

#Librarian 
    book_name = serializers.CharField(required=True)
    created_date = serializers.DateTimeField(required=True)  

    class Meta:
        model = Librarian
        fields = [
            'email', 'full_name', 'address', 'place', 'pin_code', 
            'district', 'state', 'phone_number', 'country_code', 
            'password',  'book_name', 'created_date','id'
        ]

class LibrarianDataserializer(serializers.Serializer):
    class Meta:
        model =Librarian
        fields =fields = ['user', 'book_name', 'custom_id', 'created_date']
        
class Librarianviewserializer(serializers.Serializer):
    class Meta:
        model =Librarian
        fields =' __all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class LibrarianUpdateSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    book_name = serializers.CharField(max_length=100, required=False)
    
    class Meta:
        model = Librarian
        fields = ['user', 'book_name']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        instance.user.full_name = user_data.get('full_name', instance.user.full_name)
        instance.user.address = user_data.get('address', instance.user.address)
        instance.user.place = user_data.get('place', instance.user.place)
        instance.user.pin_code = user_data.get('pin_code', instance.user.pin_code)
        instance.user.district = user_data.get('district', instance.user.district)
        instance.user.state = user_data.get('state', instance.user.state)
        instance.user.phone_number = user_data.get('phone_number', instance.user.phone_number)
        instance.user.country_code = user_data.get('country_code', instance.user.country_code)
        instance.user.save()

        instance.book_name = validated_data.get('book_name', instance.book_name)
        instance.save()
        return instance

# Serializer for Listing Librarians
class LibrarianDataSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Librarian
        fields = ['custom_id', 'book_name', 'created_date', 'user']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = {
            'email': instance.user.email,
            'full_name': instance.user.full_name,
            'address': instance.user.address,
            'place': instance.user.place,
            'pin_code': instance.user.pin_code,
            'district': instance.user.district.name if instance.user.district else None,
            'state': instance.user.state.name,
            'phone_number': instance.user.phone_number,
            'country_code': instance.user.country_code.calling_code,
        }
        return representation

# Serializer for Librarian Deletion
class LibrarianDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Librarian
        fields = ['custom_id']


class OfficeStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfficeStaff
        fields = "__all__"  

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__" 

class LibraryHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryHistory
        fields = '__all__'


class FeesRemarksSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeesRemarks
        fields = '__all__'