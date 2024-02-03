from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .mocker import UserMocker


class BaseAuthTestCase(APITestCase):
    def setUp(self):
        self.user, self.password = UserMocker.generate_random_user()
        self.token = self.get_token()
        self.auth_header = {'Authorization': f'Bearer {self.token}'}

    def get_token(self) -> str:
        auth_uri = reverse("jwt-create")
        response = self.client.post(
            auth_uri, {"email": self.user.email, "password": self.password}
        )
        return response.data['access']


class APITests(BaseAuthTestCase):
    def test_get_current_user_info(self):
        user_uri = reverse("user-me")
        response = self.client.get(
            user_uri,
            headers=self.auth_header
        )
        self.assertEquals(response.data['email'], self.user.email)
        self.assertEquals(response.data['username'], self.user.username)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_get_current_user_fail(self):
        user_uri = reverse("user-me")
        response = self.client.get(
            user_uri,
        )
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

