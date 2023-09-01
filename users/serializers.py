from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from details.models import Subscription


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        return token


class SubscriptionSerializer(serializers.ModelSerializer):



    def create(self, validated_data):
        print(validated_data.get('course').pk)
        subscription = Subscription.objects.create(
            user=self.context['request'].user,
            course=validated_data.get('course'),
        )
        return subscription

    class Meta:
        model = Subscription
        fields = '__all__'