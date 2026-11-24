"""Start the backend in Docker or Render: python start.py."""

import os
import subprocess
import sys
from pathlib import Path

from decouple import config

BACKEND_DIR = Path(__file__).resolve().parent


def main():
    os.chdir(BACKEND_DIR)
    subprocess.run([sys.executable, "manage.py", "migrate", "--noinput"], check=True)
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
