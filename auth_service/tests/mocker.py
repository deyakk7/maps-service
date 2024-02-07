from django.contrib.auth import get_user_model
from faker import Faker

User = get_user_model()
fake = Faker()


class UserMocker:
    @staticmethod
    def generate_random_user(email: str = None, password: str = None) -> dict[str, str]:
        if password is None:
            password = fake.password()
        if email is None:
            email = fake.email()

        return {
            'username': fake.user_name(),
            'email': email,
            'password': password
        }
