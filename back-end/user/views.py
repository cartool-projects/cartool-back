from django.utils.http import urlsafe_base64_encode
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status

from cartool.utils.token_generator import OTPVerifyTokenGenerator
from user.models import User
from user.serializers import CustomTokenObtainPairSerializer, UserCreateSerializer


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class UserCreateView(CreateAPIView):
    permission_classes = [~IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

    def perform_create(self, serializer):
        serializer.save(is_active=True)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


@extend_schema(
    request=None, responses={205: OpenApiTypes.STR}
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def user_logout(request):
    token = RefreshToken()
    token.blacklist()
    return Response("Success", status=status.HTTP_205_RESET_CONTENT)
