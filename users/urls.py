from django.urls import path
from users.apps import UsersConfig
from users.views import SubscriptionCreateAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('subscription/create/', SubscriptionCreateAPIView.as_view(), name='subscription_create'),
]