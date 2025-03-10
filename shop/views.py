from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Course, Category

def index_view(request):
    sort_option = request.GET.get('sort', '')
    courses = Course.objects.all()
    categories = Category.objects.all()

    courses = sort_courses_view(courses, sort_option)
    return render(request, 'shop/courses.html', {'courses': courses, 'categories': categories, 'sort_option': sort_option})


def categories_courses_view(request, category_id):
    sort_option = request.GET.get('sort', '')
    category = get_object_or_404(Category, pk=category_id)
    courses = Course.objects.filter(category=category)
    categories = Category.objects.all()

    courses = sort_courses_view(courses, sort_option)
    return render(request, 'shop/courses.html', {'courses': courses, 'categories': categories, 'sort_option': sort_option})


def single_course_view(request, course_id):
    # try:
    #     course = Course.objects.get(pk=course_id)
    #     return render(request, 'single_course.html', {'course': course})
    # except Course.DoesNotExist:
    #     raise Http404()

    course = get_object_or_404(Course, pk=course_id)
    categories = Category.objects.all()
    return render(request, 'shop/single_course.html', {'course': course, 'categories': categories})


def sort_courses_view(courses, sort_option):
    if sort_option == 'popularity':
        return courses.order_by('-students_qty')
    elif sort_option == 'new':
        return courses.order_by('-created_at')
    elif sort_option == 'price_asc':
        return courses.order_by('price')
    elif sort_option == 'price_desc':
        return courses.order_by('-price')
    return courses

def search_courses_view(request):
    sort_option = request.GET.get('sort', '')
    search_query = request.GET.get("search", "").strip()

    if search_query:
        search_courses = Course.objects.filter(title__icontains=search_query)
    else:
        search_courses = Course.objects.all()
    categories = Category.objects.all()

    courses = sort_courses_view(search_courses, sort_option)
    return render(
        request,
        "shop/courses.html",
        {"courses": courses, "sort_option": sort_option, "categories": categories, "search": search_query},
    )



"""ИЗМЕНИТЬ"""
def basket_view(request):
    basket_courses = Course.objects.all()
    categories = Category.objects.all()
    return render(
        request,
        "shop/basket.html",
        {"basket_courses": basket_courses, "categories": categories, "total_price": 112},
    )

