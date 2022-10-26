from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Creates a superuser if it doesn't exist"

    def add_arguments(self, parser):
        parser.add_argument('--username', help="Admin's username")
        parser.add_argument('--email', help="Admin's email")
        parser.add_argument('--password', help="Admin's password")

    def handle(self, *args, **kwargs):
        user = get_user_model()
        if not user.objects.filter(username=kwargs['username']).exists():
            user.objects.create_superuser(username=kwargs['username'],
                                          email=kwargs['email'],
                                          password=kwargs['password'])
