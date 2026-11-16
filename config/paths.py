"""Where things live on disk.

Every path in the app is built from `BASE_DIR`, so the project works no matter
which folder it is cloned into or which folder the server is started from.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
ENV_FILE = BASE_DIR / ".env"
