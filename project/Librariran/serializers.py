from django import forms
from accounts.models import *

class LibraryHistorySerializer(forms.ModelForm):
    class Meta:
        model = LibraryHistory
        fields = '__all__'
        
class FeesHistorySerializer(forms.ModelForm):
    class Meta:
        model = FeesRemarks
        fields = '__all__'
