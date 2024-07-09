from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from datetime import date
import re
from aqua_auth.models import Gender, UserTypes, CustomerUser

phone_number = re.compile(r"^0[71][0-9]{8}$")  # validate phone number
country_db_file = "resources/sql/kenya.sql"

ADMIN_FIRST_NAME = "Admin"
ADMIN_LAST_NAME = "Admin"
ADMIN_PHONE_NUMBER = "0712345678"
ADMIN_EMAIL = "admin@account.com"
ADMIN_DEFAULT_PASSWORD = "Admin123."


class Command(BaseCommand):
    help = "Creating the default data into the database for initial configuration of the server"

    def handle(self, *args, **options) -> str | None:

        # Add gender choices
        self.stdout.write(self.style.SUCCESS("Populating Gender table..."))
        try:
            Gender.objects.create(gender="Male")
            Gender.objects.create(gender="Female")
            Gender.objects.create(gender="Other")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Gender Creation: {e}"))
        finally:
            self.stdout.write("Exiting genders population")

        # Populate user types
        self.stdout.write(self.style.SUCCESS("Populating User Types table..."))
        try:
            UserTypes.objects.create(user_type="Admin")
            UserTypes.objects.create(user_type="Customer")
            UserTypes.objects.create(user_type="Employee")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"User type Creation: {e}"))
        finally:
            self.stdout.write("Exiting user types population")

        # Create admin user
        self.stdout.write(self.style.SUCCESS("Creating admin..."))
        try:
            gender = Gender.objects.get(id=3)
            user_type = UserTypes.objects.get(id=1)
            user = CustomerUser.objects.create(
                first_name=ADMIN_FIRST_NAME,
                last_name=ADMIN_LAST_NAME,
                gender=gender,
                phone=ADMIN_PHONE_NUMBER,
                email=ADMIN_EMAIL,
                password=ADMIN_DEFAULT_PASSWORD,
                verified=True,
                user_type=user_type,
                is_superuser=True,
                is_staff=True,
            )
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f"Admin Created Successfully!\n {user}")
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"User type Creation: {e}"))
        finally:
            self.stdout.write("Exiting user types population")
