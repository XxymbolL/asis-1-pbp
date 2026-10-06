import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Session",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("topic", models.CharField(max_length=120)),
                ("description", models.TextField()),
                (
                    "level",
                    models.CharField(
                        choices=[
                            ("basic", "Dasar"),
                            ("intermediate", "Menengah"),
                            ("advanced", "Lanjutan"),
                        ],
                        default="basic",
                        max_length=20,
                    ),
                ),
                ("scheduled_at", models.DateTimeField()),
                ("duration_minutes", models.PositiveIntegerField(default=60)),
            ],
        ),
    ]

