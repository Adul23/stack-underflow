"""Start the backend in Docker or Render: python start.py."""

import os
import subprocess
import sys
from pathlib import Path

from decouple import config

BACKEND_DIR = Path(__file__).resolve().parent

# Runs inside `manage.py shell`: create the admin, or promote an existing user and reset its password.
ENSURE_ADMIN = """
import os
from apps.users.models import CustomUser

email = os.environ["DJANGO_SUPERUSER_EMAIL"].strip()
user, created = CustomUser.objects.get_or_create(
    email=email,
    defaults={
        "first_name": os.environ.get("DJANGO_SUPERUSER_FIRST_NAME", "Demo"),
        "last_name": os.environ.get("DJANGO_SUPERUSER_LAST_NAME", "Admin"),
    },
)
user.is_staff = True
user.is_superuser = True
user.is_active = True
user.set_password(os.environ["DJANGO_SUPERUSER_PASSWORD"])
user.save()
print(f"ADMIN READY: {email} (created={created}, is_staff={user.is_staff})", flush=True)
"""


def ensure_admin():
    email = config("DJANGO_SUPERUSER_EMAIL", default="").strip()
    password = config("DJANGO_SUPERUSER_PASSWORD", default="")
    if not email or not password:
        print("ADMIN SKIPPED: DJANGO_SUPERUSER_EMAIL or DJANGO_SUPERUSER_PASSWORD is not set", flush=True)
        return
    result = subprocess.run([sys.executable, "manage.py", "shell", "-c", ENSURE_ADMIN], check=False)
    if result.returncode != 0:
        print(f"ADMIN FAILED: exit code {result.returncode} (see the error above)", flush=True)


def main():
    os.chdir(BACKEND_DIR)
    subprocess.run([sys.executable, "manage.py", "migrate", "--noinput"], check=True)
    ensure_admin()
    if config("SEED_DEMO_DATA", default=True, cast=bool):
        subprocess.run([sys.executable, "seed_demo.py"], check=True)
    subprocess.run([sys.executable, "manage.py", "collectstatic", "--noinput"], check=True)
    # Replace this process so Docker/Render signals reach the web server directly.
    os.execv(sys.executable, [
        sys.executable, "-m", "daphne", "-b", "0.0.0.0", "-p",
        os.environ.get("PORT", "8000"), "stack_underflow.asgi:application",
    ])


if __name__ == "__main__":
    main()
