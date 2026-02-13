from django.urls import path
from . import views

app_name = "shop"
urlpatterns = [
    path("", views.index_view, name="index"),
    path("all_courses", views.courses_view, name="all_courses"),
    path("<int:course_id>/", views.single_course_view, name="single_course"),
    path(
        "category/<int:category_id>/",
        views.categories_courses_view,
        name="categories_courses",
    ),
    path("search_courses/", views.search_courses_view, name="search_courses"),
    path("cart/", views.cart_view, name="cart"),
    path("add_rating/", views.add_rating_view, name="add_rating"),
    path("add_to_cart/<int:course_id>/", views.add_to_cart_view, name="add_to_cart"),
    path(
        "remove_from_cart/<int:cart_item_id>/",
        views.remove_from_cart_view,
        name="remove_from_cart",
    ),
    path("order/", views.order_view, name="order"),
]
