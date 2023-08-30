
from users.apps import UsersConfig
from django.urls import path
from .views import (TokenObtain, TokenRefreshView)
from users.views import SubscriptionCreateAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('subscription/create/', SubscriptionCreateAPIView.as_view(), name='subscription_create'),
    path('token/', TokenObtain.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]