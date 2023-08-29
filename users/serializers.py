from rest_framework import serializers

from details.models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        print(validated_data.get('course').pk)
        subscription = Subscription.objects.create(user=self.context['request'].user, course=validated_data.get('course'),
        )
        return subscription

    class Meta:
        model = Subscription
        fields = '__all__'