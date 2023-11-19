"""
WSGI config for Airline project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Airline.settings')

# Run startup code! (Runs only once before the FIRST runserver command.)==================

# =========================================================================================

application = get_wsgi_application()
