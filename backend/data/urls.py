from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FileUploadView, FinanceDataView, FinanceDataListView, FinanceDataDetailView

router = DefaultRouter()
router.register(r'file_upload', FileUploadView, basename='file_upload')
router.register(r'view_data', FinanceDataView, basename='view_data')

urlpatterns = [
    path('', include(router.urls)),
    path('finance-data/', FinanceDataListView.as_view(), name='finance-data-list'),
    path('finance-data/<int:pk>/', FinanceDataDetailView.as_view(), name='finance-data-detail'),
]