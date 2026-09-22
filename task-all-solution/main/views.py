from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import redirect, render

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
