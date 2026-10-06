from django.urls import path

from main.views import (
    create_session,
    create_session_ajax,
    get_sessions_json,
    login_user,
    logout_user,
    register_user,
    show_account,
    show_main,
    show_sessions,
)


app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("sessions/", show_sessions, name="show_sessions"),
    path("sessions/add/", create_session, name="create_session"),
    path("sessions/add-ajax/", create_session_ajax, name="create_session_ajax"),
    path("api/sessions/", get_sessions_json, name="get_sessions_json"),
    path("register/", register_user, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path("account/", show_account, name="show_account"),
]
