from django.contrib import admin
from .models import Course, Category, Lecturer, Rating, Cart, CartItem, Order

admin.site.site_header = "Courses Admin"
admin.site.site_title = "My Courses"
admin.site.index_title = "Welcome to the Courses admin area"


# class CourseAdmin(admin.ModelAdmin):
#     list_display = ('title', 'price', 'category')
#
#
# class CoursesInline(admin.TabularInline):
#     model = Course
#     exclude = ['created_at']
#     extra = 1
#
#
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('title', 'created_at')
#     fieldsets = [
#         (None, {'fields': ['title']}),
#         ('Dates', {
#             'fields': ['created_at'],
#             'classes': ['collapse']
#         })
#     ]
#     inlines = [CoursesInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
    list_display_links = ("title",)


@admin.register(Lecturer)
class LecturerAdmin(admin.ModelAdmin):
    list_display = ("id", "surname")
    list_display_links = ("surname",)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
    )
    list_display_links = ("title",)
    search_fields = ("title",)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
    )
    list_display_links = ("id",)
    search_fields = ("id",)


admin.site.register(Rating)
admin.site.register(CartItem)
admin.site.register(Order)
