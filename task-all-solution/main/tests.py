import json
from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Session


class SessionPageTest(TestCase):
    def setUp(self):
        self.session = Session.objects.create(
            topic="Membaca alur MVT",
            description="Latihan menelusuri request dari URL sampai template.",
            level="intermediate",
            scheduled_at=timezone.now() + timedelta(days=1),
            duration_minutes=75,
        )

    def test_session_model_uses_topic_as_string(self):
        self.assertEqual(str(self.session), "Membaca alur MVT")

    def test_session_url_uses_expected_template(self):
        response = self.client.get(reverse("main:show_sessions"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "session_list.html")
        self.assertContains(response, f'href="{reverse("main:create_session")}"')

    def test_session_page_displays_model_data(self):
        response = self.client.get(reverse("main:show_sessions"))

        self.assertContains(response, self.session.topic)
        self.assertContains(response, self.session.description)
        self.assertContains(response, "Menengah")
        self.assertContains(response, "75 menit")

    def test_session_page_displays_empty_state(self):
        Session.objects.all().delete()
        response = self.client.get(reverse("main:show_sessions"))

        self.assertContains(response, "Belum ada sesi belajar.")

    def test_sessions_are_ordered_by_schedule(self):
        earlier_session = Session.objects.create(
            topic="Mengenal model Django",
            description="Latihan mendefinisikan data dengan ORM.",
            level="basic",
            scheduled_at=timezone.now(),
        )
        response = self.client.get(reverse("main:show_sessions"))

        self.assertEqual(
            list(response.context["session_list"]),
            [earlier_session, self.session],
        )

    def test_main_page_links_to_session_page(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertContains(response, f'href="{reverse("main:show_sessions")}"')

    def test_create_session_saves_valid_post(self):
        response = self.client.post(
            reverse("main:create_session"),
            {
                "topic": "Membuat form Django",
                "description": "Latihan mengirim data melalui POST.",
                "level": "advanced",
                "scheduled_at": "2026-10-01T09:30",
                "duration_minutes": 90,
            },
        )

        self.assertRedirects(response, reverse("main:show_sessions"))
        self.assertTrue(Session.objects.filter(topic="Membuat form Django").exists())

    def test_create_session_shows_invalid_form(self):
        response = self.client.post(reverse("main:create_session"), {})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "session_form.html")
        self.assertContains(response, 'class="form-error"')
        self.assertContains(response, f'href="{reverse("main:show_sessions")}"')

    def test_sessions_json_filters_by_topic(self):
        other_session = Session.objects.create(
            topic="Dasar routing",
            description="Latihan path dan named route.",
            level="basic",
            scheduled_at=timezone.now() + timedelta(days=2),
        )
        response = self.client.get(
            reverse("main:get_sessions_json"),
            {"topic": "alur"},
        )
        payload = json.loads(response.content)

        self.assertEqual(response["Content-Type"], "application/json")
        self.assertEqual(len(payload), 1)
        self.assertEqual(payload[0]["pk"], str(self.session.pk))
        self.assertNotEqual(payload[0]["pk"], str(other_session.pk))
