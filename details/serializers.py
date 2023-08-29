from rest_framework import serializers

from details.models import Course, Lesson, Subscription, Payment



class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"

class CourseSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    lessons_count = serializers.IntegerField(source="lessons.count", read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)


    def get_is_subscribed(self, instance):
        request = self.context['request']
        subscription = Subscription.objects.filter(user=request.user, course=instance)
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



