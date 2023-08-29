from rest_framework.generics import CreateAPIView


from users.serializers import SubscriptionSerializer


class SubscriptionCreateAPIView(CreateAPIView):
    serializer_class = SubscriptionSerializer

