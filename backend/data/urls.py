from django.urls import path
from .views import FileUploadView

urlpatterns = [
    # Add other URL patterns as needed
    path('', FileUploadView.as_view(), name='file_upload'),
]
