from django.db import models
from django.utils import timezone

from config import settings
from users.models import User

NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name="название")
    preview = models.ImageField(verbose_name="обложка", **NULLABLE)
    description = models.TextField(verbose_name="описание", **NULLABLE)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="владелец",
        **NULLABLE,
    )

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=100, verbose_name="название")
    description = models.TextField(verbose_name="описание", **NULLABLE)
    preview = models.ImageField(verbose_name="обложка", **NULLABLE)
    video_url = models.URLField(verbose_name="ссылка на видео", **NULLABLE)
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        verbose_name="Курс",
        **NULLABLE,
        related_name="lessons",
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="владелец",
        **NULLABLE,
    )

    def __str__(self):
        return self.title


class Payment(models.Model):
    CARD = "Безналичный"
    CASH = "Наличные"

    PAYMENT_METHOD = [
        (CARD, "Безналичный"),
        (CASH, "Наличные"),
    ]

    user = models.ForeignKey(
        User, default=1, on_delete=models.CASCADE, verbose_name="пользователь"
    )
    datetime = models.DateTimeField(default=timezone.now, verbose_name="Дата и время")
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, default=1, verbose_name="курс"
    )
    amount = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="сумма")
    method = models.CharField(
        max_length=100, choices=PAYMENT_METHOD, verbose_name="способ оплаты"
    )
    is_paid = models.BooleanField(default=False, verbose_name="оплачено")
    payment_intent_id = models.CharField(default='NULL', max_length=100, verbose_name="id_платежа")

    def __str__(self):
        return f"{self.user.username}, {self.course.title}, {self.amount}"


class Subscription(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name='курс', related_name='subscription'
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="пользователь", related_name='subscription', **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name="активна")