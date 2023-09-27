from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IncomeCategoriesView, ExpensesCategoriesView


router = DefaultRouter()
router.register(r'income-category', IncomeCategoriesView, basename='income-category')
router.register(r'expenses-category', ExpensesCategoriesView, basename='expenses-category')


urlpatterns = [
    path('', include(router.urls)),
]