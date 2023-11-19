import pytest
from django.core import management


@pytest.fixture(scope="function", autouse=True)
def clean_db(django_db_blocker): 
    with django_db_blocker.unblock():
        management.call_command('flush', verbosity=0, interactive=False, database='default',)
