from django.core.management.base import BaseCommand
from faker import Faker

from posts.services import create_post

from backend.users.models import User


class Command(BaseCommand):
    help = "Adds posts to the database"

    def handle(self, *args, **options):
        fake = Faker()

        faker_user = User.objects.get(username="faker")

        for _ in range(100):
            title = fake.sentence(
                nb_words=6, variable_nb_words=True, ext_word_list=None
            )
            body = fake.text(max_nb_chars=200, ext_word_list=None)
            create_post(creator=faker_user, title=title, body=body)

        print("Completed!!! Check your database.")
