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
