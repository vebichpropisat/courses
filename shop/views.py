from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpRequest, HttpResponse
from .models import Course, Category, Rating, Cart, CartItem, Order
from django.db.models import Sum


COURSES_SORT_MAPPING = {
    "popularity": "-students_qty",
    "new": "-created_at",
    "price_asc": "price",
    "price_desc": "-price",
}


def index_view(request: HttpRequest) -> HttpResponse:
    categories = Category.objects.all()

    return render(
        request,
        "shop/index.html",
        {"categories": categories},
    )


def courses_view(request: HttpRequest) -> HttpResponse:
    sort_option = request.GET.get("sort", "")
    courses = Course.objects.select_related("category").all()
    categories = Category.objects.all()

    courses = sort_courses_view(courses, sort_option)
    return render(
        request,
        "shop/courses.html",
        {"courses": courses, "categories": categories, "sort_option": sort_option},
    )


def categories_courses_view(request: HttpRequest, category_id: int) -> HttpResponse:
    sort_option = request.GET.get("sort", "")
    category = get_object_or_404(Category, pk=category_id)
    courses = Course.objects.filter(category=category).select_related("category")
    categories = Category.objects.all()

    courses = sort_courses_view(courses, sort_option)
    return render(
        request,
        "shop/courses.html",
        {"courses": courses, "categories": categories, "sort_option": sort_option},
    )


def single_course_view(request: HttpRequest, course_id: int) -> HttpResponse:
    course = get_object_or_404(
        Course.objects.select_related("category", "lecturer"), pk=course_id
    )
    categories = Category.objects.all()
    return render(
        request, "shop/single_course.html", {"course": course, "categories": categories}
    )


def sort_courses_view(courses: "QuerySet", sort_option: str) -> "QuerySet":
    sort_by = COURSES_SORT_MAPPING.get(sort_option)
    if sort_by := COURSES_SORT_MAPPING.get(sort_option):
        return courses.order_by(sort_by)
    return courses


def search_courses_view(request: HttpRequest) -> HttpResponse:
    sort_option = request.GET.get("sort", "")
    search_query = request.GET.get("search", "").strip()

    if search_query:
        search_courses = Course.objects.filter(
            title__icontains=search_query
        ).select_related("category")
    else:
        search_courses = Course.objects.all().select_related("category")
    categories = Category.objects.all()

    courses = sort_courses_view(search_courses, sort_option)
    return render(
        request,
        "shop/courses.html",
        {
            "courses": courses,
            "sort_option": sort_option,
            "categories": categories,
            "search": search_query,
        },
    )


def add_rating_view(request: HttpRequest) -> JsonResponse:
    if request.method == "POST":
        course_id = request.POST.get("course")
        star = request.POST.get("star")

        course = get_object_or_404(Course, id=course_id)

        rating, created = Rating.objects.update_or_create(
            user=request.user, course=course, defaults={"star": star}
        )

        avg_rating = course.average_rating()
        return JsonResponse({"success": True, "avg_rating": round(avg_rating, 1)})

    return JsonResponse({"success": False}, status=400)


def add_to_cart_view(request: HttpRequest, course_id: int) -> JsonResponse:
    if request.method == "POST":
        course = get_object_or_404(Course, id=course_id)
        cart, created = Cart.objects.get_or_create(user=request.user, status="active")
        if CartItem.objects.filter(cart__user=request.user, course=course).exists():
            return JsonResponse({"success": False}, status=400)

        CartItem.objects.create(cart=cart, course=course, price=course.price)
        return JsonResponse({"success": True, "message": "Курс додано в кошик"})

    return JsonResponse({"success": False}, status=400)


def cart_view(request: HttpRequest) -> HttpResponse:
    cart_courses = CartItem.objects.filter(
        cart__user=request.user, cart__status="active"
    ).select_related("cart", "course")
    categories = Category.objects.all()
    total_price = cart_courses.aggregate(Sum("price"))["price__sum"] or 0
    return render(
        request,
        "shop/cart.html",
        {
            "cart_courses": cart_courses,
            "categories": categories,
            "total_price": total_price,
        },
    )


def remove_from_cart_view(request: HttpRequest, cart_item_id: int) -> JsonResponse:
    if request.method == "POST":
        cart_item = get_object_or_404(CartItem, id=cart_item_id)
        cart_item.delete()
        return JsonResponse({"success": True, "message": "Курс видалений з кошика"})

    return JsonResponse(
        {"success": False, "message": "Invalid request method"}, status=400
    )


def order_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        cart = get_object_or_404(Cart, user=request.user, status="active")
        cart.status = "ordered"
        cart.save()
        Order.objects.create(
            user=request.user, cart=cart, price=request.POST.get("price").replace(',', '.')
        )
        return redirect("shop:index")

    return redirect("shop:cart")
