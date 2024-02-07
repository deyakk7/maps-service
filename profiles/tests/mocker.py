from faker import Faker

fake = Faker()


class ProfileMocker:
    @staticmethod
    def generate_random_profile():
        return {
            "bio": fake.text(),
            "address": fake.address(),
        }
