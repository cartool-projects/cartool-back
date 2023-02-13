from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import LoginView, UserCreateView, user_logout

app_name = 'user'

router = SimpleRouter()

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', UserCreateView.as_view(), name='register'),
    path('logout/', user_logout, name='logout'),
] + router.urls