from django.urls import path
from .views import LibraryHistoryView,FeesHistoryView

urlpatterns = [
    path('library-history/', LibraryHistoryView.as_view(), name='library_history_list'),
    path('fees-history/', FeesHistoryView.as_view(), name='fees_history_list'),
    ]
