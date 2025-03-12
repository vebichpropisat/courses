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
    poster = models.ImageField("Постер", upload_to="courses_images/")
    price = models.FloatField()
    description = models.TextField()
    students_qty = models.IntegerField()
    reviews_qty = models.IntegerField()
    lecturer = models.ForeignKey(
        Lecturer,
        verbose_name="викладач",
        related_name="course_lecturer",
        on_delete=models.CASCADE,
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def average_rating(self):
        ratings = Rating.objects.filter(course=self)
        if ratings.exists():
            return sum(rating.star for rating in ratings) / ratings.count()
        return 0

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курси"


class Rating(models.Model):
    """Рейтинг"""

    user = models.ForeignKey(
        User, verbose_name="користувач", on_delete=models.CASCADE, default=""
    )
    star = models.PositiveSmallIntegerField("зірки", default=1)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="курс")

    def __str__(self):
        return f"{self.star} - {self.course}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"
        unique_together = ("user", "course")


class Cart(models.Model):
    """Кошик"""

    user = models.ForeignKey(User, verbose_name="користувач", on_delete=models.CASCADE)
    status = models.CharField(max_length=300, default="active")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Кошик {self.user.username}"

    class Meta:
        verbose_name = "Кошик"
        verbose_name_plural = "Кошики"


class CartItem(models.Model):
    """Товар в кошику"""

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name="курс", on_delete=models.CASCADE)
    price = models.FloatField()

    def __str__(self):
        return f"{self.course.title} у кошику {self.cart.user.username}"

    class Meta:
        verbose_name = "Товар в кошику"
        verbose_name_plural = "Товари в кошику"


class Order(models.Model):
    """Замовлення"""

    user = models.ForeignKey(User, verbose_name="користувач", on_delete=models.CASCADE)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    price = models.FloatField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Замовлення {self.id} - {self.user.username})"

    class Meta:
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"
