from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Category(models.Model):
    """Категорії/Мова програмування"""

    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"


class Lecturer(models.Model):
    """Викладачі"""

    surname = models.CharField("Прізвище", max_length=20, default=None)
    name = models.CharField("Ім'я", max_length=20)

    def __str__(self):
        return f"{self.surname} {self.name}"

    class Meta:
        verbose_name = "Викладач"
        verbose_name_plural = "Викладачі"


class Course(models.Model):
    """Курси"""

    title = models.CharField(max_length=300)
    price = models.FloatField()
    students_qty = models.IntegerField()
    reviews_qty = models.IntegerField()
    lecturers = models.ForeignKey(Lecturer, verbose_name="викладач", related_name="course_lecturer", on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курси"


class RatingStar(models.Model):
    """Зірка рейтингу"""

    value = models.SmallIntegerField("Значення", default=0)

    def __str__(self):
        return f"{self.value}"

    class Meta:
        verbose_name = "Зірка рейтингу"
        verbose_name_plural = "Зірки рейтингу"
        ordering = ["-value"]


class Rating(models.Model):
    """Рейтинг"""

    user = models.ForeignKey(User, verbose_name="користувач", on_delete=models.CASCADE, default='')
    star = models.ForeignKey(RatingStar, verbose_name="зірка", on_delete=models.CASCADE)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name="курс"
    )

    def __str__(self):
        return f"{self.star} - {self.course}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"
