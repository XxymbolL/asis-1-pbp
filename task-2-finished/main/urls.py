from django.urls import path

from main.views import show_main, show_sessions


app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("sessions/", show_sessions, name="show_sessions"),
]
