from django.urls import path

from details.apps import DetailsConfig
from rest_framework.routers import DefaultRouter
from details.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, CourseCreateAPIView
from details.views import CourseDestroyAPIView, CourseUpdateAPIView, CourseRetrieveAPIView, PaymentListAPIView, \
    PaymentCreateAPIView, PaymentDestroyAPIView, PaymentUpdateAPIView, PaymentRetrieveAPIView

from django.urls import path


app_name = DetailsConfig.name

router = DefaultRouter()
router.register(r"courses", CourseViewSet, basename="courses")

urlpatterns = [
                  path("lessons/create/", LessonCreateAPIView.as_view(), name="lesson-create"),
                  path("lessons/", LessonListAPIView.as_view(), name="lesson-list"),
                  path("lessons/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson-get"),
                  path(
                      "lessons/update/<int:pk>/", LessonUpdateAPIView.as_view(), name="lesson-update"
                  ),
                  path(
                      "lessons/delete/<int:pk>/", LessonDestroyAPIView.as_view(), name="lesson-delete"
                  ),
                  path("course/create/", CourseCreateAPIView.as_view(), name="create-course"),
                  path("course/<int:pk>/", CourseRetrieveAPIView.as_view(), name="course-get"),
                  path(
                      "course/update/<int:pk>/", CourseUpdateAPIView.as_view(), name="course-update"
                  ),
                  path(
                      "course/delete/<int:pk>/", CourseDestroyAPIView.as_view(), name="course-delete"
                  ),
                  path("payment/create/", PaymentCreateAPIView.as_view(), name="payment-create"),
                  path("payment/", PaymentListAPIView.as_view(), name="payment-list"),
                  path("payment/<int:pk>/", PaymentRetrieveAPIView.as_view(), name="payment-get"),
                  path(
                      "payment/update/<int:pk>/",
                      PaymentUpdateAPIView.as_view(),
                      name="payment-update",
                  ),
                  path(
                      "payment/delete/<int:pk>/",
                      PaymentDestroyAPIView.as_view(),
                      name="payment-delete",
                  ),

              ] + router.urls
