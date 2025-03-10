from django.urls import path

from . import views

app_name = 'auth_app'
urlpatterns = [
    path("registration/", views.register_view, name="register"),
    path("log_in/", views.login_view, name="log_in"),
    path("exit/", views.logout_view, name="exit"),
]
