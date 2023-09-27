from rest_framework.routers import DefaultRouter
from .views import ExpensesViewSet


router = DefaultRouter()
router.register(r"", ExpensesViewSet)

urlpatterns = router.urls

