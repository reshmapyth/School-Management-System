from django.contrib import admin
from .models import  District, State,  User, Country_Codes,OfficeStaff,Librarian,Student,LibraryHistory,FeesRemarks

admin.site.register(User)
admin.site.register(Country_Codes)
admin.site.register(District)
admin.site.register(State)
admin.site.register(OfficeStaff)
admin.site.register(Librarian)
admin.site.register(Student)
admin.site.register(LibraryHistory)
admin.site.register(FeesRemarks)