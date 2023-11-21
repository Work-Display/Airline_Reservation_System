from django.test import TestCase
import pytest
from ...airline_reservation_system.facade import *

# pytest .\tests\airline_reservation_system\test_facade.py::Test_Get_Instances_By_Name
@pytest.mark.skip
class Test_Get_Instances_By_Name(TestCase):

    @pytest.mark.django_db()
    def test_get_instances_by_name(self):

        # Correct use: ===============================================
        
        role_FD = {'role_name': 'Administrator'}
        role_name = 'Administrator'
        assert(validate_user_role(role_name=role_name))
        DAL.add_instance(some_model=User_Roles, field_data=role_FD)
        

        # Wrong uses: ===============================================
        assert(not(validate_user_role(role_name=role_name))) # when it already exists

        role_name = {'role_name': 'Cat'}
        assert(not(validate_user_role(role_name=role_name)))

        role_name = {'role_name': 5}
        assert(not(validate_user_role(role_name=role_name)))

        assert(not(validate_user_role(role_name=role_FD)))
