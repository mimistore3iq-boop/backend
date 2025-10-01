"""
WSGI config for ecom_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import sys
import os
from pathlib import Path

from django.core.wsgi import get_wsgi_application

# Add the backend directory to the Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_project.settings')

application = get_wsgi_application()