from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
import os

User = get_user_model()

class Command(BaseCommand):
    help = "Create admin user automatically for Render Free"

    def handle(self, *args, **kwargs):
        username = os.environ.get("ADMIN_USERNAME")
        email = os.environ.get("ADMIN_EMAIL")
        password = os.environ.get("ADMIN_PASSWORD")

        if not username or not password:
            print("Admin credentials not provided")
            return

        if User.objects.filter(username=username).exists():
            print("Admin already exists")
            return

        User.objects.create_superuser(username=username, email=email, password=password)
        print("Superuser created successfully")
