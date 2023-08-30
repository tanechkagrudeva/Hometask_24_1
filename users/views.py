
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.serializers import MyTokenObtainPairSerializer, SubscriptionSerializer


class TokenObtain(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class SubscriptionCreateAPIView(CreateAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]