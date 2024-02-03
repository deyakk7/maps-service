from django.urls import reverse
from rest_framework import status

from auth_service.tests.tests import BaseAuthTestCase
from .mocker import EventsAndReviewsMocker
from ..models import Event, Review
from auth_service.tests.mocker import UserMocker


class EventsTests(BaseAuthTestCase):
    def setUp(self):
        super().setUp()
        self.event = self.create_event()

    def create_event(self):
        event_data = EventsAndReviewsMocker.generate_random_event()
        return Event.objects.create(**event_data, user_id=self.user.id)

    def test_get_all_events_fail(self):
        event_uri: str = reverse('events-list')
        response = self.client.get(
            event_uri,
        )
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_all_events(self):
        event_uri: str = reverse('events-list')
        response = self.client.get(
            event_uri,
            headers=self.auth_header
        )

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_create_event_fail(self):
        event_uri: str = reverse('events-list')
        response = self.client.post(
            event_uri,
            EventsAndReviewsMocker.generate_random_event()
        )
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_event(self):
        event_uri: str = reverse('events-list')
        response = self.client.post(
            event_uri,
            EventsAndReviewsMocker.generate_random_event(),
            headers=self.auth_header
        )
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_get_current_user_events(self):
        event_uri = reverse('events-for-user')
        response = self.client.get(
            event_uri,
            headers=self.auth_header,
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)


class ReviewTests(EventsTests):
    def setUp(self):
        super().setUp()
        self.review_uri = reverse('reviews-list', kwargs={'pk': self.event.id})

    def create_reviews(self, user_id=None) -> Review:
        if user_id is None:
            user_id = self.user.id

        return Review.objects.create(
            user_id=user_id,
            event_id=self.event.id,
            **EventsAndReviewsMocker.generate_random_review()
        )

    def test_get_all_reviews(self):
        response = self.client.get(
            self.review_uri,
            headers=self.auth_header
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_create_review_fail(self):
        response = self.client.post(
            self.review_uri,
            EventsAndReviewsMocker.generate_random_review(),
        )
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_review(self):
        response = self.client.post(
            self.review_uri,
            EventsAndReviewsMocker.generate_random_review(),
            headers=self.auth_header
        )
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_check_rating_when_new_review_added(self):
        result_rating = 0
        tests_count = 5
        for _ in range(tests_count):
            user, password = UserMocker.generate_random_user()
            review = self.create_reviews(user_id=user.id)
            result_rating += review.rating

        self.event.refresh_from_db()
        result_rating /= 5
        self.assertEquals(self.event.rating, result_rating)
        self.assertEquals(self.event.total_reviews, tests_count)
