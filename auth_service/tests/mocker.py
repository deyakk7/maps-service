from django.contrib.auth import get_user_model
from faker import Faker

User = get_user_model()
fake = Faker()


class UserMocker:
    @staticmethod
    def generate_random_user() -> tuple[User, str]:
        password = fake.password()
        return User.objects.create_user(
            username=fake.user_name(),
            email=fake.email(),
            password=password
        ), password
