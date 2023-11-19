from django.test import TestCase
import pytest
from airline_reservation_system.dal import *
from airline_reservation_system.models import *
import datetime as dt
from django.core.files.uploadedfile import SimpleUploadedFile

# pytest .\tests\airline_reservation_system\test_dal.py

# CRUD: =====================================

# @pytest.mark.now
class Test_DAL_Get_Instance_By_ID(TestCase):

    @pytest.mark.django_db()
    def test_DAL_get_instance_by_id(self):
        # Correct uses: ===============================================
        role_FD = {'role_name': 'Administrator'}
        DAL.add_instance(some_model=User_Roles, field_data=role_FD)
        role = DAL.get_instance_by_id(some_model=User_Roles, id=1)
        assert(role)

        user_FD = {'username':'usemyname', 'email':'fake@mail.com', 'password':'A1b2C3d4', 'user_role_id':role.id}
        DAL.add_instance(some_model=Users, field_data=user_FD)
        user = DAL.get_instance_by_id(some_model=Users, id=1)
        assert(user)

        customer_FD = {'first_name':'Bernard', 'last_name':'Wiseman', 'address':'Germany, Zeon, spacecol.78.', 
                    'phone_no':'+49 163 09083378', 'credit_card_no':'4929493965436444', 'user_id_id':user.id}
        DAL.add_instance(some_model=Customers, field_data=customer_FD)
        customer = DAL.get_instance_by_id(some_model=Customers, id=1)
        assert(customer)

        admin_FD = {'first_name':'Bernard', 'last_name':'Wiseman', 'user_id_id':user.id}
        DAL.add_instance(some_model=Administrators, field_data=admin_FD)
        admin = DAL.get_instance_by_id(some_model=Administrators, id=1)
        assert(admin)

        country_FD = {'name':'Finland'}
        DAL.add_instance(some_model=Countries, field_data=country_FD)
        country = DAL.get_instance_by_id(some_model=Countries, id=1)
        assert(country)

        country_FD = {'name':'Germany'}
        DAL.add_instance(some_model=Countries, field_data=country_FD)
        country2 = Countries.objects.get(name='Finland')

        airline_FD = {'name':'Cyclops-Ace', 'country_id_id':country2.id, 'user_id_id':user.id}
        DAL.add_instance(some_model=Airline_Companies, field_data=airline_FD)
        airline = DAL.get_instance_by_id(some_model=Airline_Companies, id=1)
        assert(airline)

        # departure = dt.datetime.now(tz=pytz.UTC) # NTS: changed USE_TZ settings to False so this isn't needed unless I change it back.
        departure = dt.datetime.now()
        landing = departure + timedelta(hours=3)
        flight_FD = {'airline_company_id_id':airline.id, 'origin_country_id_id':country.id, 'destination_country_id_id':country2.id, 'departure_time':departure, 'landing_time':landing, 'remaining_tickets':54}
        DAL.add_instance(some_model=Flights, field_data=flight_FD)
        flight = DAL.get_instance_by_id(some_model=Flights, id=1)
        assert(flight)

        tickets_FD = {'flight_id_id':flight.id, 'customer_id_id':customer.id}
        DAL.add_instance(some_model=Tickets, field_data=tickets_FD)
        tickets = DAL.get_instance_by_id(some_model=Tickets, id=1)
        assert(tickets)

        # Wrong uses: ===============================================
        class Poodle:
            pass
        try:
            poodle = DAL.get_instance_by_id(some_model=Poodle, id=1)
            assert type(poodle) is str
        except:
            pass

        try:
            role = DAL.get_instance_by_id(some_model=User_Roles, id=-1)
            assert type(role) is str
        except:
            pass

        try:
            role = DAL.get_instance_by_id(some_model=User_Roles, id='abc')
            assert type(role) is str
        except:
            pass


def test_DAL_get_all_instances():
    pass

@pytest.mark.django_db
def test_DAL():
    User_Roles.objects.create()
    assert User_Roles.objects.count() == 1

class Test_DAL_Add_Instance(TestCase):

    @pytest.mark.django_db()
    def test_DAL_add_instance(self):
        # Correct uses: ===============================================
        role_FD = {'role_name': 'Administrator'}
        DAL.add_instance(some_model=User_Roles, field_data=role_FD)
        role = User_Roles.objects.get(role_name='Administrator')
        assert(role)

        user_FD = {'username':'usemyname', 'email':'fake@mail.com', 'password':'A1b2C3d4', 'user_role_id':role.id}
        DAL.add_instance(some_model=Users, field_data=user_FD)
        user = Users.objects.get(username='usemyname')
        # count = Users.objects.all().count()
        # print('users : ',count)
        assert(user)

        thumbnail = SimpleUploadedFile(name='test_image.jpg', content=open("./images2test/yeah.webp", 'rb').read(), content_type='image/jpeg')
        user_FD = {'username':'usemynametoo', 'email':'fake2@mail.com', 'password':'A1b2C3d4', 'user_role_id':role.id, 'thumbnail':thumbnail}
        DAL.add_instance(some_model=Users, field_data=user_FD)
        user2 = Users.objects.get(username='usemynametoo')
        assert(user2)

        customer_FD = {'first_name':'Bernard', 'last_name':'Wiseman', 'address':'Germany, Zeon, spacecol.78.', 
                    'phone_no':'+49 163 09083378', 'credit_card_no':'4929493965436444', 'user_id_id':user.id}
        DAL.add_instance(some_model=Customers, field_data=customer_FD)
        customer = Customers.objects.get(phone_no='+49 163 09083378')
        assert(customer)

        admin_FD = {'first_name':'Bernard', 'last_name':'Wiseman', 'user_id_id':user.id}
        DAL.add_instance(some_model=Administrators, field_data=admin_FD)
        admin = Administrators.objects.get(user_id_id=user.id)
        assert(admin)

        flag = SimpleUploadedFile(name='fi.png', content=open("./images2test/fi.png", 'rb').read(), content_type='image/jpeg')
        country_FD = {'name':'Finland', 'flag': flag}
        DAL.add_instance(some_model=Countries, field_data=country_FD)
        country = Countries.objects.get(name='Finland')
        assert(country)

        flag = SimpleUploadedFile(name='de.png', content=open("./images2test/de.png", 'rb').read(), content_type='image/jpeg')
        country_FD = {'name':'Germany', 'flag': flag}
        DAL.add_instance(some_model=Countries, field_data=country_FD)
        country2 = Countries.objects.get(name='Germany')

        airline_FD = {'name':'Cyclops-Ace', 'country_id_id':country2.id, 'user_id_id':user.id}
        DAL.add_instance(some_model=Airline_Companies, field_data=airline_FD)
        airline = Airline_Companies.objects.get(user_id_id=user.id)
        assert(airline)

        # departure = dt.datetime.now(tz=pytz.UTC)
        departure = dt.datetime.now()
        landing = departure + timedelta(hours=3)
        flight_FD = {'airline_company_id_id':airline.id, 'origin_country_id_id':country.id, 'destination_country_id_id':country2.id, 'departure_time':departure, 'landing_time':landing, 'remaining_tickets':54}
        DAL.add_instance(some_model=Flights, field_data=flight_FD)
        flight = Flights.objects.get(remaining_tickets=54)
        assert(flight)

        tickets_FD = {'flight_id_id':flight.id, 'customer_id_id':customer.id}
        DAL.add_instance(some_model=Tickets, field_data=tickets_FD)
        tickets = Tickets.objects.get(customer_id_id=customer.id)
        assert(tickets)

        # Wrong uses: ===============================================
        class Poodle:
            pass
        try:
            poodle_FD = {'flight_id_id':flight.id, 'customer_id_id':customer.id}
            DAL.add_instance(some_model=Poodle, field_data=tickets_FD)
            poodle = Tickets.objects.get(customer_id_id=customer.id)
            assert type(poodle) is str
        except:
            pass

        try:
            bad_role_FD = ["don'tfailme"]
            DAL.add_instance(some_model=User_Roles, field_data=bad_role_FD)
            role = User_Roles.objects.get(role_name='Administrator')
            assert type(role) is str
        except:
            pass

        try:
            role_FD = {'cat_name': 'Administrator'}
            DAL.add_instance(some_model=User_Roles, field_data=role_FD)
            role = User_Roles.objects.get(role_name='Administrator')
            assert type(role) is str
        except:
            pass

        try:
            role_FD = {'role_name': 123}
            DAL.add_instance(some_model=User_Roles, field_data=role_FD)
            role = User_Roles.objects.get(role_name='Administrator')
            assert type(role) is str
        except:
            pass


def test_DAL_add_all_instances():
    pass

def test_DAL_update_instance():
    pass

def test_DAL_remove_instance():
    pass

# get specifics: ==============================

def test_get_user_by_username():
    pass

def test_get_customer_by_username():
    pass

def test_get_airlines_by_countryID():
    pass

def test_get_airline_by_username():
    pass

def test_get_airlines_by_parameters():
    pass

def test_get_flights_by_origin_countyID():
    pass

def test_get_flights_by_destination_countyID():
    pass

def test_get_flights_by_departure_date():
    pass

def test_get_flights_by_landing_date():
    pass

def test_get_flights_by_customerID():
    pass

def test_get_flights_by_parameters():
    pass

def test_get_flights_by_airlineID():
    pass

def test_get_arriving_flights():
    pass

def test_get_departing_flights():
    pass

def test_get_tickets_by_customer():
    pass


# pytest .\tests\airline_reservation_system\test_dal.py::Test_Populate_Countries
@pytest.mark.skip # This one should work only if you run it from the root directory of the project.
class Test_Populate_Countries(TestCase):

    @pytest.mark.django_db()
    def test_populate_countries(self):
        
        assert(populate_countries())
        country = Countries.objects.get(id=1)
        assert(country)
        country = Countries.objects.get(id=249)
        assert(country)


# @pytest.mark.now
class Test_Validate_Get_Role_By_User(TestCase):

    @pytest.mark.django_db()
    def test_get_role_by_user(self):

        # Correct uses: ===============================================
        
        if (populate_user_roles()):
            roles = {1:'Administrator', 2:'Airline Company', 3:'Customer'}
            
            user_FD = {'username':'usemyname1', 'email':'fake@mail1.com', 'password':'A1b2C3d4', 'user_role_id':1} 
            DAL.add_instance(some_model=Users, field_data=user_FD)
            assert((get_role_by_user(user_id=1)) == roles[1])
            assert(not((get_role_by_user(user_id=1)) == (val for key, val in roles)))

            user_FD = {'username':'usemyname2', 'email':'fake@mail2.com', 'password':'A1b2C3d4', 'user_role_id':2} 
            DAL.add_instance(some_model=Users, field_data=user_FD)
            assert((get_role_by_user(user_id=2)) == roles[2])
            

            user_FD = {'username':'usemyname3', 'email':'fake@mail3.com', 'password':'A1b2C3d4', 'user_role_id':3} 
            DAL.add_instance(some_model=Users, field_data=user_FD)
            assert((get_role_by_user(user_id=3)) == roles[3])
            

            # Wrong uses: ===============================================
            
            assert(not((get_role_by_user(user_id=1)) == 'Pet'))

            assert(not((get_role_by_user(user_id=398)) == (val for key, val in roles)))

            assert(not((get_role_by_user(user_id='meow')) == (val for key, val in roles)))

        else:
            error_msg = "ERROR. 'populate_user_roles' failed. Test can't be done."
            logger.error(error_msg)
            assert(False)



