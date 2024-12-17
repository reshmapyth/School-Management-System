from django.urls import include, path
from .views import CommonloginView
from . import views



urlpatterns = [
    path('login/', CommonloginView.as_view(), name='common-login'),
    
]