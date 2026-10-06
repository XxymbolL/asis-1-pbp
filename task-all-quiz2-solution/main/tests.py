import json
from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

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
        self.assertContains(response, f'href="{reverse("main:login")}"')

    def test_session_page_provides_the_json_contract_for_javascript(self):
        response = self.client.get(reverse("main:show_sessions"))

        self.assertContains(response, f'data-api-url="{reverse("main:get_sessions_json")}"')
        self.assertContains(response, 'src="/static/js/sessions.js"')
        self.assertContains(response, 'id="session-loading"')

    def test_session_page_displays_empty_state(self):
        Session.objects.all().delete()
        response = self.client.get(reverse("main:get_sessions_json"))

        self.assertEqual(response.json(), [])

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

    def test_register_creates_and_logs_in_user(self):
        response = self.client.post(
            reverse("main:register"),
            {
                "username": "peserta",
                "password1": "latihan-aman-123",
                "password2": "latihan-aman-123",
            },
        )

        self.assertRedirects(response, reverse("main:show_sessions"))
        self.assertTrue(User.objects.filter(username="peserta").exists())
        self.assertEqual(self.client.session.get("_auth_user_id"), str(User.objects.get(username="peserta").pk))

    def test_login_sets_cookie_and_logout_deletes_it(self):
        User.objects.create_user(username="peserta", password="latihan-aman-123")
        response = self.client.post(
            reverse("main:login"),
            {"username": "peserta", "password": "latihan-aman-123"},
        )

        self.assertRedirects(response, reverse("main:show_sessions"))
        self.assertIn("last_login", response.cookies)

        response = self.client.get(reverse("main:logout"))
        self.assertRedirects(response, reverse("main:show_main"))
        self.assertEqual(response.cookies["last_login"]["max-age"], 0)

    def test_account_requires_login_and_displays_cookie(self):
        response = self.client.get(reverse("main:show_account"))
        self.assertRedirects(response, f'{reverse("main:login")}?next={reverse("main:show_account")}')

        user = User.objects.create_user(username="peserta", password="latihan-aman-123")
        self.client.force_login(user)
        self.client.cookies["last_login"] = "baru saja"
        response = self.client.get(reverse("main:show_account"))

        self.assertContains(response, "peserta")
        self.assertContains(response, "baru saja")

    def test_session_page_shows_dialog_only_to_authenticated_user(self):
        response = self.client.get(reverse("main:show_sessions"))
        self.assertNotContains(response, 'id="session-dialog"')

        self.client.force_login(User.objects.create_user(username="peserta", password="latihan-aman-123"))
        response = self.client.get(reverse("main:show_sessions"))
        self.assertContains(response, 'id="session-dialog"')
        self.assertContains(response, 'id="open-session-dialog"')

    def test_ajax_create_requires_login(self):
        response = self.client.post(reverse("main:create_session_ajax"), {})

        self.assertEqual(response.status_code, 302)

    def test_ajax_create_returns_json_for_valid_and_invalid_form(self):
        self.client.force_login(User.objects.create_user(username="peserta", password="latihan-aman-123"))
        valid_response = self.client.post(
            reverse("main:create_session_ajax"),
            {
                "topic": "Fetch dan DOM",
                "description": "Latihan mengubah respons JSON menjadi elemen halaman.",
                "level": "advanced",
                "scheduled_at": "2026-10-07T13:00",
                "duration_minutes": 90,
            },
            HTTP_ACCEPT="application/json",
        )
        invalid_response = self.client.post(reverse("main:create_session_ajax"), {})

        self.assertEqual(valid_response.status_code, 201)
        self.assertEqual(valid_response.json()["message"], "Sesi Fetch dan DOM berhasil ditambahkan.")
        self.assertTrue(Session.objects.filter(topic="Fetch dan DOM").exists())
        self.assertEqual(invalid_response.status_code, 400)
        self.assertIn("topic", invalid_response.json()["errors"])
