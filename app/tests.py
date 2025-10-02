from __future__ import annotations

from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Event, Member, User


class PublicPagesTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_homepage_accessible(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_events_page_accessible(self):
        response = self.client.get(reverse("events_list"))
        self.assertEqual(response.status_code, 200)


class MemberModelTests(TestCase):
    def test_member_string_representation(self):
        member = Member.objects.create(
            first_name="Mario",
            last_name="Rossi",
            email="mario.rossi@example.com",
        )
        self.assertEqual(str(member), "Mario Rossi")


class AuthenticatedViewsTests(TestCase):
    def setUp(self) -> None:
        self.member = Member.objects.create(
            first_name="Laura",
            last_name="Bianchi",
            email="laura@example.com",
            role=Member.ROLE_AMMINISTRATORE,
        )
        self.user = User.objects.create_user(
            username="laura",
            password="password123",
            member=self.member,
            role=Member.ROLE_AMMINISTRATORE,
        )
        self.client = Client()
        self.client.login(username="laura", password="password123")

    def test_dashboard_requires_admin(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_event_creation_flow(self):
        response = self.client.post(
            reverse("event_create"),
            {
                "title": "Assemblea",
                "description": "Incontro annuale",
                "date": (timezone.now() + timezone.timedelta(days=1)).strftime("%Y-%m-%dT%H:%M"),
                "location": "Sede centrale",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Event.objects.count(), 1)
