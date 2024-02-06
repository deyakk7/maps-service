from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from auth_service.tests.mocker import UserMocker
from auth_service.tests.tests import BaseAuthTestCase
from .mocker import EventsAndReviewsMocker
from ..models import Event

User = get_user_model()


class EventsTests(BaseAuthTestCase):
    def setUp(self):
        super().setUp()
        self.event = self.create_event()
        self.event_uri = reverse('events-list')
        self.event_uri_id = reverse('events-detail', kwargs={'pk': self.event.id})
        self.event_uri_my = reverse('events-for-user')

    def create_event(self):
        event_data = EventsAndReviewsMocker.generate_random_event()
        return Event.objects.create(**event_data, user_id=self.user.id)

    def test_get_all_events_fail(self):
        response = self.client.get(
            self.event_uri,
        )
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_all_events(self):
        response = self.client.get(
            self.event_uri,
            headers=self.auth_header
        )

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_create_event_fail(self):
        response = self.client.post(
            self.event_uri,
            EventsAndReviewsMocker.generate_random_event()
        )
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_event(self):
        response = self.client.post(
            self.event_uri,
            EventsAndReviewsMocker.generate_random_event(),
            headers=self.auth_header
        )
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_get_current_user_events(self):
        response = self.client.get(
            self.event_uri_my,
            headers=self.auth_header,
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_change_event_not_auth_fail(self):
        response = self.client.put(
            self.event_uri,
            EventsAndReviewsMocker.generate_random_event(),
        )

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_change_event_another_user_fail(self):
        new_user, user_password = UserMocker.generate_random_user()
        new_user_token = self.get_token(new_user.email, user_password)
        new_auth_headers = {'Authorization': f'Bearer {new_user_token}'}

        response = self.client.put(
            self.event_uri_id,
            EventsAndReviewsMocker.generate_random_event(),
            headers=new_auth_headers
        )

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_change_event(self):
        new_data = EventsAndReviewsMocker.generate_random_event()
        response = self.client.put(
            self.event_uri_id,
            new_data,
            headers=self.auth_header,
        )

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['title'], new_data['title'])

    def test_delete_event_auth_fail(self):
        response = self.client.delete(
            self.event_uri_id,
        )
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_event(self):
        response = self.client.delete(
            self.event_uri_id,
            headers=self.auth_header
        )

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
