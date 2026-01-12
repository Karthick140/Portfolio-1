import sys, os

# Set up the path to your application
sys.path.append(os.getcwd())

# Import your Flask app instance
# Ensure your app instance is named 'app' in app.py
from app import app as application
