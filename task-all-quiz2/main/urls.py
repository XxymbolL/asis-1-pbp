from django.urls import path

from main.views import create_session, get_sessions_json, show_main, show_sessions


# TODO Tugas 1, 2, dan 5: Import view autentikasi, akun, dan endpoint AJAX.


app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("sessions/", show_sessions, name="show_sessions"),
    path("sessions/add/", create_session, name="create_session"),
    path("api/sessions/", get_sessions_json, name="get_sessions_json"),
    # TODO Tugas 1: Tambahkan route register, login, dan logout.
    # TODO Tugas 2: Tambahkan route halaman akun.
    # TODO Tugas 5: Tambahkan route POST /sessions/add-ajax/.
]
