from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import ProductViewSet, CategoryViewSet

router = SimpleRouter()
router.register('products', ProductViewSet, basename='products')

urlpatterns = [
    path('categories/', CategoryViewSet.as_view(), name='categories'),
] + router.urls