from django.shortcuts import render

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
