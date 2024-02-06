from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from auth_service.tests.mocker import UserMocker
from .mocker import EventsAndReviewsMocker
from .test_events import EventsTests
from ..models import Review

User = get_user_model()


class ReviewTests(EventsTests):
    def setUp(self):
        super().setUp()
        self.review_uri = reverse('reviews-list', kwargs={'pk': self.event.id})

    def create_review(self, user_id=None, event_id=None) -> Review:
        if user_id is None:
            user_id = self.user.id

        if event_id is None:
            event_id = self.event.id

        return Review.objects.create(
            user_id=user_id,
            event_id=event_id,
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
            review = self.create_review(user_id=user.id)
            result_rating += review.rating

        self.event.refresh_from_db()
        result_rating /= tests_count
        self.assertEquals(self.event.rating, result_rating)
        self.assertEquals(self.event.total_reviews, tests_count)

    def test_check_rating_when_deleting_review(self):
        tests_count = 5
        sum_of_rating = 0
        review: Review | None = None

        for _ in range(tests_count):
            user, password = UserMocker.generate_random_user()
            review = self.create_review(user_id=user.id)
            sum_of_rating += review.rating

        result_rating = sum_of_rating / 5
        self.event.refresh_from_db()
        self.assertEquals(self.event.rating, result_rating)

        sum_of_rating -= review.rating
        review.delete()
        tests_count -= 1
        result_rating = sum_of_rating / tests_count

        self.event.refresh_from_db()
        self.assertEquals(self.event.rating, result_rating)
        self.assertEquals(self.event.total_reviews, tests_count)

    def test_change_review_auth_fail(self):
        response = self.client.put(
            self.review_uri,
            EventsAndReviewsMocker.generate_random_review()
        )

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_change_review_another_user_fail(self):
        review = self.create_review()
        review_uri_id = reverse('reviews-detail', kwargs={'pk': review.id})

        new_user, user_password = UserMocker.generate_random_user()
        new_user_token = self.get_token(new_user.email, user_password)
        new_auth_headers = {'Authorization': f'Bearer {new_user_token}'}

        response = self.client.put(
            review_uri_id,
            EventsAndReviewsMocker.generate_random_review(),
            headers=new_auth_headers
        )

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_change_review(self):
        review = self.create_review()
        review_uri_id = reverse('reviews-detail', kwargs={'pk': review.id})

        new_data = EventsAndReviewsMocker.generate_random_review()
        response = self.client.put(
            review_uri_id,
            new_data,
            headers=self.auth_header,
        )

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['rating'], new_data['rating'])
