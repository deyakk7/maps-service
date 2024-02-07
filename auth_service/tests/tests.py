from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .mocker import UserMocker

User = get_user_model()


class BaseAuthTestCase(APITestCase):
    def setUp(self):
        user_data = UserMocker.generate_random_user()
        self.password = user_data['password']
        self.user, self.auth_header = self.create_user(email=user_data['email'], password=user_data['password'])
        self.token = self.get_token()

    def get_token(self, user_email=None, user_password=None) -> str:
        if user_email is None:
            user_email = self.user.email
        if user_password is None:
            user_password = self.password

        auth_uri: str = reverse("jwt-create")
        response = self.client.post(
            auth_uri, {"email": user_email, "password": user_password}
        )
        return response.data['access']

    def create_user(self, email: str = None, password: str = None) -> tuple[User, dict]:
        user_data = UserMocker.generate_random_user(email=email, password=password)
        user = User.objects.create_user(
            **user_data
        )
        return user, self.get_auth_headers(user_data['email'], user_data['password'])

    def get_auth_headers(self, email: str, password: str) -> dict:
        token: str = self.get_token(email, password)
        headers: dict = {'Authorization': f'Bearer {token}'}
        return headers


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
