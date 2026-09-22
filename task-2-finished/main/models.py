import uuid

from django.db import models


class Session(models.Model):
    LEVEL_CHOICES = [
        ("basic", "Dasar"),
        ("intermediate", "Menengah"),
        ("advanced", "Lanjutan"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    topic = models.CharField(max_length=120)
    description = models.TextField()
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default="basic")
    scheduled_at = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(default=60)

    def __str__(self):
        return self.topic

