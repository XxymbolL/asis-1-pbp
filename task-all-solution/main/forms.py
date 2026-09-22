from django import forms

from main.models import Session


class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ["topic", "description", "level", "scheduled_at", "duration_minutes"]
        widgets = {
            "scheduled_at": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
        }
