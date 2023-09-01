from rest_framework import serializers
from details.services import create_payment, retrieve_payment, make_payment
from details.models import Course, Lesson, Payment, Subscription
from details.validators import TitleValidator, URLValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class LessonCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [
            URLValidator(field="video_url"),
            serializers.UniqueTogetherValidator(
                fields=("video_url",), queryset=Lesson.objects.all()
            ),
        ]


class CourseCreateSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = "__all__"
        validators = [
            TitleValidator(field="title"),
            serializers.UniqueTogetherValidator(
                fields=("title",), queryset=Course.objects.all()
            ),
        ]

    def create(self, validated_data):
        course = Course.objects.create(owner=self.context['request'].user, **validated_data)
        return course


class CourseSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    lessons_count = serializers.IntegerField(source="lessons.count", read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)

    def get_is_subscribed(self, instance):
        request = self.context['request']
        subscription = Subscription.objects.filter(user=request.user,
                                                   course=instance)
        if subscription:
            return True
        return False

    class Meta:
        model = Course
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class PaymentCreateSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['payment_intent_id'] = create_payment(int(validated_data.get('amount')))
        payment = Payment.objects.create(**validated_data)
        return payment

    class Meta:
        model = Payment
        fields = "__all__"


class PaymentRetrieveSerializer(serializers.ModelSerializer):
    payment_status = serializers.SerializerMethodField()

    def get_payment_status(self, instance):
        return retrieve_payment(instance.payment_intent_id)

    class Meta:
        model = Payment
        fields = "__all__"


class PaymentUpdateSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        payment = make_payment(instance.payment_intent_id)
        if payment == 'succeeded':
            instance.is_paid = True
            instance.save()
            return instance
        else:
            return instance

    class Meta:
        model = Payment
        fields = "__all__"

