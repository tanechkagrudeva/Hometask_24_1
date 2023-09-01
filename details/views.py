from rest_framework import viewsets, generics
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from details.tasks import send_course_update_email
from details.models import Course, Lesson, Payment
from details.paginators import CoursePaginator
from details.permissions import IsOwner, IsNotStuff, IsStuff
from details.serializers import (
    CourseSerializer,
    LessonSerializer,
    PaymentSerializer,
    CourseCreateSerializer, LessonCreateSerializer, PaymentCreateSerializer, PaymentRetrieveSerializer,
    PaymentUpdateSerializer,
)


class CourseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = CourseSerializer
    pagination_class = CoursePaginator
    queryset = Course.objects.all()


    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff or not self.request.user.is_authenticated:
            return queryset
        return queryset.filter(owner=self.request.user)


class CourseCreateAPIView(generics.CreateAPIView):
    """
    API endpoint that allows users to create courses.
    """
    serializer_class = CourseCreateSerializer
    permission_classes = [IsNotStuff]


class CourseUpdateAPIView(generics.UpdateAPIView):
    """
    API endpoint that allows users to update courses.
    """
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    # permission_classes = [IsOwner, IsStuff]

    def patch(self, request, *args, **kwargs):
        print("Patching")
        instance = self.get_object()  # Получение объекта курса
        subscribers = instance.subscription.filter(is_active=True)
        for subscriber in subscribers:
            send_course_update_email.delay(instance.title, subscriber.user.email)

        return super().update(request, *args, **kwargs)


class CourseDestroyAPIView(generics.DestroyAPIView):
    """
    API endpoint that allows users to delete courses.
    """
    queryset = Course.objects.all()
    permission_classes = [IsOwner]


class CourseRetrieveAPIView(generics.RetrieveAPIView):
    """
    API endpoint that allows users to retrieve course.
    """
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsOwner]


class LessonCreateAPIView(generics.CreateAPIView):
    """
    API endpoint that allows users to create lessons.
    """
    serializer_class = LessonCreateSerializer
    permission_classes = [IsNotStuff]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    """
    API endpoint that allows users to retrieve lessons.
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """
    API endpoint that allows users to retrieve lesson.
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    """
    API endpoint that allows users to update lesson.
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner, IsStuff]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """
    API endpoint that allows users to delete lesson.
    """
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner]


class PaymentCreateAPIView(generics.CreateAPIView):
    """
    API endpoint that allows users to create payments.
    """
    serializer_class = PaymentCreateSerializer


class PaymentListAPIView(generics.ListAPIView):
    """
    API endpoint that allows users to retrieve payments.
    """
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_fields = (
        "method",
        "course",
    )
    search_fields = ["course", "method"]
    ordering_fields = ["datetime"]


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    """
    API endpoint that allows users to retrieve payment.
    """
    serializer_class = PaymentRetrieveSerializer
    queryset = Payment.objects.all()


class PaymentUpdateAPIView(generics.UpdateAPIView):
    """
    API endpoint that allows users to update payment.
    """
    serializer_class = PaymentUpdateSerializer
    queryset = Payment.objects.all()


class PaymentDestroyAPIView(generics.DestroyAPIView):
    """
    API endpoint that allows users to delete payment.
    """
    queryset = Payment.objects.all()
