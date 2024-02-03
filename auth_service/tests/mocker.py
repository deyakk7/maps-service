from django.test import TestCase
from ..models import User

from faker import Faker

fake = Faker()


class UserMocker:
    @staticmethod
    def generate_random_user():
        password = fake.password()
        return User.objects.create_user(
            username=fake.user_name(),
            email=fake.email(),
            password=password
        ), password
