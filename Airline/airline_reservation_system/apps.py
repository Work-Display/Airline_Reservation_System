from django.apps import AppConfig
import sys
from django.core import management


import logging 
logger = logging.getLogger("pick.me") 

class AirlineReservationSystemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'airline_reservation_system'

    def ready(self): # RTS: This runs every time the server reloads.

        if ('runserver' in sys.argv): 
            return True
        
        # If runserver wasn't run yet, and migrations are complete, DO THIS ONCE:
        management.call_command("makemigrations", no_input=True)
        management.call_command("migrate", no_input=True)
        from .utiles import populate_all
        if not(populate_all()):
            logger.error(f"Failed to populate the database with the initial data of ARS.")
            return False
        logger.info(f"Successfully populated the database with the initial data of ARS.")
        return True