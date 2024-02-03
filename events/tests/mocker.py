from django.utils import timezone
from datetime import timedelta

from faker import Faker

fake = Faker()


class EventsAndReviewsMocker:
    @staticmethod
    def generate_random_event() -> dict:
        current_date = timezone.now()
        return {
            'title': fake.name(),
            'description': fake.text(),
            'start_date': current_date,
            'end_date': current_date + timedelta(days=15),
            'position_x': fake.pydecimal(
                left_digits=2,
                right_digits=5,
                positive=True
            ),
            'position_y': fake.pydecimal(
                left_digits=2,
                right_digits=5,
                positive=True
            )
        }

    @staticmethod
    def generate_random_review() -> dict:
        return {
            'rating': fake.random_int(min=1, max=5),
            'comment': fake.text()
        }
