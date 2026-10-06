from django.core import serializers
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from main.forms import SessionForm
from main.models import Session


def show_main(request):
    context = {
        "name": "[Nama fasilitator]",
        "study_program": "[Program studi fasilitator]",
        "bio": "Fasilitator latihan Django untuk sesi asistensi PBP.",
        "npm": "[NPM fasilitator]",
        "email": "email@example.com",
    }
    return render(request, "index.html", context)


def show_sessions(request):
    context = {
        "session_list": Session.objects.all().order_by("scheduled_at"),
        "form": SessionForm(),
    }
    return render(request, "session_list.html", context)


def create_session(request):
    form = SessionForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("main:show_sessions")
    return render(request, "session_form.html", {"form": form})


def get_sessions_json(request):
    topic_query = request.GET.get("topic", "").strip()
    sessions = Session.objects.all().order_by("scheduled_at")
    if topic_query:
        sessions = sessions.filter(topic__icontains=topic_query)
    return HttpResponse(
        serializers.serialize("json", sessions),
        content_type="application/json",
    )


def register_user(request):
    form = UserCreationForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("main:show_sessions")
    return render(request, "register.html", {"form": form})


def login_user(request):
    form = AuthenticationForm(request, data=request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        response = redirect("main:show_sessions")
        response.set_cookie("last_login", "baru saja", max_age=60 * 60 * 24)
        return response
    return render(request, "login.html", {"form": form})


def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie("last_login")
    return response


@login_required
def show_account(request):
    context = {
        "last_login": request.COOKIES.get("last_login"),
    }
    return render(request, "account.html", context)


@login_required
@require_POST
def create_session_ajax(request):
    form = SessionForm(request.POST)
    if form.is_valid():
        session = form.save()
        return JsonResponse(
            {
                "message": f"Sesi {session.topic} berhasil ditambahkan.",
                "id": str(session.pk),
            },
            status=201,
        )
    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)
