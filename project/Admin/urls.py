from django.urls import path
from .views import LibrarianRegister, LibrarianData,LibrarianUpdate,OfficeStaffRegister,OfficeStaffCreateView,OfficeStaffRetrieveView,OfficeStaffUpdateView, OfficeStaffDeleteView,StudentDetailView,StudentUpdateView,StudentDeleteView,StudentListView

urlpatterns = [
    path('librarian/register/', LibrarianRegister.as_view(), name='librarian-register'),
    path('librarian/list/', LibrarianData.as_view(), name='librarian-list'),
    path('librarian/update/', LibrarianUpdate.as_view(), name='librarian-update'),
    path('librarian/delete/', LibrarianUpdate.as_view(), name='delete_librarian'),
    path('officestaff/register/', OfficeStaffRegister.as_view(), name='delete_librarian'),
    path('office-staff/create/', OfficeStaffCreateView.as_view(), name='office_staff_create'),
    path('office-staff/<int:pk>/', OfficeStaffRetrieveView.as_view(), name='office_staff_retrieve'),
    path('office-staff/<int:pk>/update/', OfficeStaffUpdateView.as_view(), name='office_staff_update'),
    path('office-staff/<int:pk>/delete/', OfficeStaffDeleteView.as_view(), name='office_staff_delete'),
    path('student/<int:pk>/', StudentDetailView.as_view(), name='student_detail'),
    path('student/<int:pk>/update/', StudentUpdateView.as_view(), name='student_update'),
    path('student/<int:pk>/delete/', StudentDeleteView.as_view(), name='student_delete'),
    path('students/', StudentListView.as_view(), name='student_list'),
]
