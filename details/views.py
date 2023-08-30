from rest_framework import viewsets, generics
from details.models import Course, Lesson, Payment
from details.serializers import LessonSerializer, CourseSerializer, PaymentSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from details.permissions import IsOwner, IsNotStuff, IsStuff
from details.paginators import CoursePaginator



class CourseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = CourseSerializer
    pagination_class = CoursePaginator
    queryset = Course.objects.all()


class CourseCreateAPIView(generics.CreateAPIView):
    """
    API endpoint that allows users to create courses.
    """
    serializer_class = CourseSerializer
    permission_classes = [IsNotStuff]


class CourseUpdateAPIView(generics.UpdateAPIView):
    """
    API endpoint that allows users to update courses.
    """
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


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
    serializer_class = LessonSerializer
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


