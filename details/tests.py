from rest_framework import status
from rest_framework.test import APITestCase
from details.models import Course, Lesson, Subscription
from users.models import User


class CourseTestCase(APITestCase):
    def create_user(self):
        """User creation test"""
        self.user = User.objects.create(
            email='test@sky.pro',
            is_active=True,
        )
        self.user.set_password('test')
        self.user.save()

    def setUp(self) -> None:
        self.user = User.objects.create(email='test@example.com', password='test')
        self.course = Course.objects.create(title='test', owner=self.user)
        self.data = {
            'course': self.course,
            'title': 'test',
            'owner': self.user
        }

        self.lesson = Lesson.objects.create(**self.data)
        self.client.force_authenticate(user=self.user)
        self.subscription = Subscription.objects.create(course=self.course, user=self.user)

    def test_course_create(self):
        """Test creating a new course"""
        data = {
            "title": "Test Course",
            "description": "This is a test course",
            "lessons": [],
        }
        response = self.client.post("/courses/", data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["title"], data["title"])
        self.assertTrue(Course.objects.all().exists())

    def test_list_courses(self):
        """Test listing courses"""
        response = self.client.get("/courses/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_course(self):
        """Test getting a course"""
        response = self.client.get(f"/courses/{self.course.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["title"], self.course.title)

    def test_update_course(self):
        """Test updating a course"""
        data = {
            "title": "Test Course",
            "description": "This is a test course",
            "lessons": [],
        }
        response = self.client.put(f"/courses/{self.course.pk}/", data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["title"], data["title"])

    def test_delete_course(self):
        """Test deleting a course"""
        response = self.client.delete(f"/courses/{self.course.pk}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Course.objects.all().exists())

    def test_lesson_create(self):
        """Test creating a new lesson"""
        data = {
            'course': self.course.pk,
            'title': 'test lesson',
            'owner': self.user.pk,
            'video_url': "https://youtube.com/jnikniun"
        }
        response = self.client.post("/lessons/create/", data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["title"], data["title"])
        self.assertTrue(Lesson.objects.all().exists())

    def test_list_lessons(self):
        """Test listing lessons"""
        response = self.client.get("/lessons/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_lesson(self):
        """Test getting a lesson"""
        response = self.client.get(f"/lessons/{self.lesson.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["title"], self.lesson.title)

    def test_update_lesson(self):
        """Test updating a lesson"""
        self.user.is_staff = True
        data = {
            'course': self.course.pk,
            'title': 'updated test lesson',
            'owner': self.user.pk,
            'video_url': "https://youtube.com/jnikniun"
        }
        response = self.client.put(f"/lessons/update/{self.lesson.pk}/", data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["title"], data["title"])

    def test_delete_lesson(self):
        """Test deleting a lesson"""
        response = self.client.delete(f"/lessons/delete/{self.lesson.pk}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.all().exists())

    def test_active_subscription(self):
        response = self.client.get(f"/courses/{self.course.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.json()["is_subscribed"])