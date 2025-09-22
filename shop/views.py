from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpRequest, HttpResponse
from .models import Course, Category, Rating, Cart, CartItem, Order
from django.db.models import Sum
from django.core.cache import cache
from django.core.paginator import Paginator
from functools import wraps
from .documents import CourseDocument
import hashlib


COURSES_SORT_MAPPING = {
    "popularity": "-students_qty",
    "new": "-created_at",
    "price_asc": "price",
    "price_desc": "-price",
}

def redis_cache(timeout=60):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(*args, **kwargs):
            cache_key = hashlib.md5(f"{view_func.__name__}:{args}:{kwargs}".encode()).hexdigest()

            cached_context = cache.get(cache_key)
            if cached_context:
                print("кеш")
                return cached_context

            context = view_func(*args, **kwargs)
            cache.set(cache_key, context, timeout=timeout)

            return context
        return _wrapped_view
    return decorator


def paginate(courses, page_number, items_per_page=12):
    paginator = Paginator(courses, items_per_page)
    page_obj = paginator.get_page(page_number)
    courses = page_obj.object_list

    return courses, page_obj


def sort_courses_view(courses: "QuerySet", sort_option: str) -> "QuerySet":
    if sort_by := COURSES_SORT_MAPPING.get(sort_option):
        return courses.order_by(sort_by)
    return courses


@redis_cache(timeout=60*60*2)
def get_categories():
    categories = Category.objects.all()
    return categories


def index_view(request: HttpRequest) -> HttpResponse:
    categories = get_categories()

    return render(
        request,
        "shop/index.html",
        {"categories": categories},
    )


def get_courses(sort_option, page_number=None):
    courses = Course.objects.select_related("category").all()
    categories = get_categories()

    courses = sort_courses_view(courses, sort_option)
    courses, page_obj = paginate(courses, page_number)

    return {"courses": courses, "categories": categories, "sort_option": sort_option, "page_obj": page_obj}


def courses_view(request: HttpRequest) -> HttpResponse:
    sort_option = request.GET.get("sort", "")
    page_number = request.GET.get('page')

    context = get_courses(sort_option, page_number=page_number)

    return render(request, "shop/courses.html", context)


def get_categories_courses(category_id, sort_option, page_number=None):
    category = get_object_or_404(Category, pk=category_id)
    courses = Course.objects.filter(category=category).select_related("category")
    categories = get_categories()

    courses = sort_courses_view(courses, sort_option)
    courses, page_obj = paginate(courses, page_number)

    return {"courses": courses, "categories": categories, "sort_option": sort_option, "page_obj": page_obj}


def categories_courses_view(request: HttpRequest, category_id: int) -> HttpResponse:
    sort_option = request.GET.get("sort", "")
    page_number = request.GET.get('page')

    context = get_categories_courses(category_id, sort_option, page_number=page_number)

    return render(request, "shop/courses.html", context)


@redis_cache(timeout=60*5)
def get_single_course(course_id):
    course = get_object_or_404(Course.objects.select_related("category", "lecturer"), pk=course_id)
    categories = get_categories()
    print("БД")
    return {"course": course, "categories": categories}


def single_course_view(request: HttpRequest, course_id: int) -> HttpResponse:

    context = get_single_course(course_id)

    return render(request,"shop/single_course.html", context)


def get_search_courses(search_query, sort_option, page_number=None):
    if search_query:
        search_courses = Course.objects.filter(
            title__icontains=search_query
        ).select_related("category")
    else:
        search_courses = Course.objects.all().select_related("category")
    categories = get_categories()

    courses = sort_courses_view(search_courses, sort_option)
    courses, page_obj = paginate(courses, page_number)

    return {"courses": courses, "sort_option": sort_option, "categories": categories, "search": search_query, "page_obj": page_obj}


def search_courses_view(request: HttpRequest) -> HttpResponse:
    sort_option = request.GET.get("sort", "")
    search_query = request.GET.get("search", "").strip()
    page_number = request.GET.get('page')

    context = get_search_courses(search_query, sort_option, page_number=page_number)

    return render(request, "shop/courses.html", context)


# @paginate(items_per_page=12, object_name='courses')
# def search_courses_view(request: HttpRequest) -> tuple:
#     sort_option = request.GET.get("sort", "")
#     search_query = request.GET.get("search", "").strip()
#     search_courses = []
#
#
#     if search_query:
#         search_courses = CourseDocument.search().query("multi_match", query=search_query, fields=['title', 'description'])
#     else:
#         search_courses = Course.objects.all().select_related("category")
#     categories = Category.objects.all()
#
#     courses = sort_courses_view(search_courses, sort_option)
#     return "shop/courses.html", {                          # render() в декораторі
#             "courses": courses,
#             "sort_option": sort_option,
#             "categories": categories,
#             "search": search_query,
#         }


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
    if not request.user.is_authenticated:
        return JsonResponse({
            "success": False,
            "message": "Потрібно увійти в акаунт, щоб додати курс у кошик."
        }, status=401)

    elif request.method == "POST":
        course = get_object_or_404(Course, id=course_id)
        cart, created = Cart.objects.get_or_create(user=request.user, status="active")
        if CartItem.objects.filter(cart__user=request.user, course=course).exists():
            return JsonResponse({"success": False, "message": "Цей курс вже є у вашому кошику."}, status=400)

        CartItem.objects.create(cart=cart, course=course, price=course.price)
        return JsonResponse({"success": True, "message": "Курс додано в кошик"})

    return JsonResponse({"success": False}, status=400)


def cart_view(request: HttpRequest) -> HttpResponse:
    # if not request.user.is_authenticated:
    #     return JsonResponse({
    #         "success": False,
    #         "message": "Щоб переглянути кошик, потрібно авторизуватись."
    #     }, status=401)

    cart_courses = CartItem.objects.filter(
        cart__user=request.user, cart__status="active"
    ).select_related("cart", "course")
    categories = get_categories()
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
        try:
            cart = Cart.objects.get(user=request.user, status="active")
        except Cart.DoesNotExist:
            messages.warning(request, "Ваш кошик порожній.")
            return redirect("shop:cart")

        cart_items = CartItem.objects.filter(cart=cart)
        if not cart_items.exists():
            messages.warning(request, "Ваш кошик порожній.")
            return redirect("shop:cart")

        cart.status = "ordered"
        cart.save()

        Order.objects.create(
            user=request.user,
            cart=cart,
            price=request.POST.get("price", "0").replace(",", ".")
        )
        messages.success(request, "Замовлення успішно оформлено.")
        return redirect("shop:index")

    # if request.method == "POST":
    #     cart = get_object_or_404(Cart, user=request.user, status="active")
    #     cart.status = "ordered"
    #     cart.save()
    #     Order.objects.create(
    #         user=request.user, cart=cart, price=request.POST.get("price").replace(',', '.')
    #     )
    #     return redirect("shop:index")

    return redirect("shop:cart")
