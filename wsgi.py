import sys
from pathlib import Path

# Ensure the Flask app dir (has a space in its name) is on sys.path
PROJECT_ROOT = Path(__file__).parent
APP_DIR = PROJECT_ROOT / "AI Astrology"
if str(APP_DIR) not in sys.path:
	sys.path.insert(0, str(APP_DIR))

# Import the Flask app instance
from app import app as application  # WSGI callable
