from django.test import TestCase
import pytest
from airline_reservation_system.facade import *
from airline_reservation_system.utiles import populate_countries

# pytest .\airline_reservation_system\test_facade.py::Test_Get_Instances_By_Name
# @pytest.mark.skip
class Test_Get_Instances_By_Name(TestCase):

    @pytest.mark.django_db()
    def test_get_instances_by_name(self):

        # Correct use: ===============================================
        if not(populate_countries()):
            print("'populate_countries' failed. Can't run this test.")
            assert(False)

        str = 'Canada'
        assert(Facade_Base.get_instances_by_name(some_model=Countries, name=str))
        str = 'canada'
        assert(Facade_Base.get_instances_by_name(some_model=Countries, name=str))
        str = 'a'
        assert(Facade_Base.get_instances_by_name(some_model=Countries, name=str))
        str = 'tc'
        assert(Facade_Base.get_instances_by_name(some_model=Countries, name=str))

        # # Wrong uses: ===============================================
        str = 'zzzzzzzzzzzzzzzzzzz'
        assert(not(Facade_Base.get_instances_by_name(some_model=Countries, name=str)))

        str = 'uy4'
        assert(not(Facade_Base.get_instances_by_name(some_model=Countries, name=str)))
