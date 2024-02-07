from django.urls import reverse
from rest_framework import status

from auth_service.tests.tests import BaseAuthTestCase

from .mocker import ProfileMocker


class ProfileTestCase(BaseAuthTestCase):
    def setUp(self):
        super().setUp()

        self.profile_uri = reverse('profile-list')
        self.profile_uri_me = reverse('profile-me')

    def test_create_profile_fail(self):
        response = self.client.post(
            self.profile_uri,
            ProfileMocker.generate_random_profile(),
            headers=self.auth_header,
        )

        self.assertEquals(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_profile_auth_fail(self):
        response = self.client.put(
            self.profile_uri,
            ProfileMocker.generate_random_profile()
        )

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_profile_another_user(self):
        profile_data = ProfileMocker.generate_random_profile()
        profile_data['user_name'] = self.user.username + 'error'
        response = self.client.put(
            self.profile_uri_me,
            profile_data,
            headers=self.auth_header
        )

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['bio'], profile_data['bio'])
        self.assertNotEquals(response.data['user_name'], profile_data['user_name'])
