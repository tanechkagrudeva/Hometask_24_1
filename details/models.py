from django.db import models


from config import settings


NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    objects = None
    title = models.CharField(max_length=100, verbose_name="название")
    preview = models.ImageField(verbose_name="обложка", **NULLABLE)
    description = models.TextField(verbose_name="описание", **NULLABLE)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=100, verbose_name="название")
    description = models.TextField(verbose_name="описание", **NULLABLE)
    preview = models.ImageField(verbose_name="обложка", **NULLABLE)
    video_url = models.URLField(verbose_name="ссылка на видео", **NULLABLE)

    def __str__(self):
        return self.title



