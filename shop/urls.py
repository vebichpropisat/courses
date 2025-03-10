from django.urls import path
from . import views

app_name = 'shop'
urlpatterns = [
    path('', views.index_view, name='index'),
    path('<int:course_id>/', views.single_course_view, name='single_course'),
    path('category/<int:category_id>/', views.categories_courses_view, name='categories_courses'),
    path("search_courses/", views.search_courses_view, name="search_courses"),
    path("basket/", views.basket_view, name="basket"),
]
