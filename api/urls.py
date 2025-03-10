from django.urls import path, include
from api.models import CategoryResource, CourseResource
from tastypie.api import Api

api = Api(api_name='v1')
api.register(CategoryResource())
api.register(CourseResource())

urlpatterns = [
    path('', include(api.urls), name='index'),
]
