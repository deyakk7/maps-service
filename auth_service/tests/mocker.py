from django.test import TestCase
from ..models import User

from faker import Faker

fake = Faker()


class APIMocker:
    @staticmethod
    def generate_random_user():
        password = fake.password()
        return User.objects.create_user(
            email=fake.email(),
            password=password
        ), password
