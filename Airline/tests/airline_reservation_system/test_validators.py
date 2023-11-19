from django.test import TestCase
import pytest
from airline_reservation_system.validators import *
from airline_reservation_system.models import *
from airline_reservation_system.utiles import val_add_user
import datetime as dt
import pytz
from django.core.files.uploadedfile import SimpleUploadedFile


# pytest .\tests\airline_reservation_system\test_validators.py
# pytest .\tests\airline_reservation_system\test_validators.py::Test_Validate_User

# CRUD: =====================================

@pytest.mark.skip
class Test_Validate_User_Role(TestCase):

    @pytest.mark.django_db()
    def test_validate_user_role(self):

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

# @pytest.mark.now
class Test_Validate_User(TestCase):

    @pytest.mark.django_db()
    def test_validate_user(self):

        # Correct use: ===============================================
        
        role_FD = {'role_name': 'Administrator'}
        DAL.add_instance(some_model=User_Roles, field_data=role_FD)
        # role = DAL.get_instance_by_id(some_model=User_Roles, id=1)
        user_FD = {'username':'usemyname', 'email':'fake@mail.com', 'password':'A1b2C3d4', 'user_role':1}
        assert(validate_user(user_field_data=user_FD))

        thumbnail1 = SimpleUploadedFile(name='test_image.jpg', content=open("./images2test/yeah.webp", 'rb').read(), content_type='image/jpeg')
        user_FD = {'username':'usemyname', 'email':'fake@mail.com', 'password':'A1b2C3d4', 'user_role':1, 'thumbnail':thumbnail1}
        assert(validate_user(user_field_data=user_FD))

        # Wrong uses: ===============================================

        thumbnail2 = SimpleUploadedFile(name='dice.png', content=open("./images2test/dice.png", 'rb').read(), content_type='image/png')
        user_FD = {'username':'usemyname', 'email':'fake@mail.com', 'password':'A1b2C3d4', 'user_role':1, 'thumbnail':thumbnail2}
        assert(not(validate_user(user_field_data=user_FD))) # Should only accept '.jpg'/'.jpeg'/'.webp' image formats

        user_FD = {'username':123, 'email':'fake@mail.com', 'password':'A1b2C3d4', 'user_role':1}
        assert(not(validate_user(user_field_data=user_FD)))

        user_FD = {'username':'us', 'email':'fake@mail.com', 'password':'A1b2C3d4', 'user_role':1}
        assert(not(validate_user(user_field_data=user_FD)))

        user_FD = {'username':'usemynameeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee', 'email':'fake@mail.com', 'password':'A1b2C3d4', 'user_role':1}
        assert(not(validate_user(user_field_data=user_FD)))

        user_FD = {'username':'use#myname', 'email':'fake@mail.com', 'password':'A1b2C3d4', 'user_role':1}
        assert(not(validate_user(user_field_data=user_FD)))

        user_FD = {'username':'usemyname', 'email':123, 'password':'A1b2C3d4', 'user_role':1}
        assert(not(validate_user(user_field_data=user_FD)))

        user_FD = {'username':'usemyname', 'email':'fakemail.com', 'password':'A1b2C3d4', 'user_role':1}
        assert(not(validate_user(user_field_data=user_FD)))

        user_FD = {'username':'usemyname', 'email':'fake@mail.com', 'password':1234567, 'user_role':1}
        assert(not(validate_user(user_field_data=user_FD)))

        user_FD = {'username':'usemyname', 'email':'fake@mail.com', 'password':'A1', 'user_role':1}
        assert(not(validate_user(user_field_data=user_FD)))

        user_FD = {'username':'usemyname', 'email':'fake@mail.com', 'password':'1234567', 'user_role':1}
        assert(not(validate_user(user_field_data=user_FD)))

        user_FD = {'username':'usemyname', 'email':'fake@mail.com', 'password':'aabbccdd', 'user_role':1}
        assert(not(validate_user(user_field_data=user_FD)))

        user_FD = {'username':'usemyname', 'email':'fake@mail.com', 'password':'A1b$ccdd', 'user_role':1}
        assert(not(validate_user(user_field_data=user_FD)))

        user_FD = {'username':'usemyname', 'email':'fake@mail.com', 'password':'A1b2C3d44444444444444444444444444444444444444444', 'user_role':1}
        assert(not(validate_user(user_field_data=user_FD)))

        user_FD = {'username':'usemyname', 'email':'fake@mail.com', 'password':'A1b2C3d4', 'user_role':'hi'}
        assert(not(validate_user(user_field_data=user_FD)))

        user_FD = {'username':'usemyname', 'email':'fake@mail.com', 'password':'A1b2C3d4', 'user_role':89}
        assert(not(validate_user(user_field_data=user_FD)))

        user_FD = {'username':'usemyname', 'email':'fake@mail.com', 'password':'A1b2C3d4', 'user_role_id':1, 'thumbnail':thumbnail1} # RTS: dal FD's foreign keys should always have that redundant additional 'id' at the end.
        DAL.add_instance(some_model=Users, field_data=user_FD) #username already exists
        user_FD = {'username':'usemyname', 'email':'fake@mail.com', 'password':'A1b2C3d4', 'user_role':1, 'thumbnail':thumbnail1}
        assert(not(validate_user(user_field_data=user_FD)))

        user_FD = {'username':'usemynametoo', 'email':'fake@mail.com', 'password':'A1b2C3d4', 'user_role':1, 'thumbnail':thumbnail1} #email already exists
        assert(not(validate_user(user_field_data=user_FD)))


# @pytest.mark.now
class Test_Validate_Customer(TestCase):

    @pytest.mark.django_db()
    def test_validate_customer(self):

        # Correct use: ===============================================
        
        role_FD = {'role_name': 'Customer'}
        DAL.add_instance(some_model=User_Roles, field_data=role_FD)
        user_FD = {'username':'usemyname', 'email':'fake@mail.com', 'password':'A1b2C3d4', 'user_role_id':1}
        DAL.add_instance(some_model=Users, field_data=user_FD)
        customer_FD = {'first_name': 'Murka', 'last_name': 'Paw', 'address':'Israel, Cat-City, Meow-Street, 101/2.', 
        'phone_no':'+972 50-101-2101', 'credit_card_no':'4524 7948 2579 0782', 'user_id':1}
        assert(validate_customer(customer_field_data=customer_FD))
        
        customer_FD = {'first_name': 'Murka', 'last_name': 'Paw', 'address':'Israel, Cat-City, Meow-Street, 101/2.', 
        'phone_no':'+1 350-956-5941', 'credit_card_no':'4524 7948 2579 0782', 'user_id':1}
        assert(validate_customer(customer_field_data=customer_FD))

        customer_FD = {'first_name': 'Murka', 'last_name': 'Paw', 'address':'Israel, Cat-City, Meow-Street, 101/2.', 
        'phone_no':'+54 9 3865 51-2516', 'credit_card_no':'4524 7948 2579 0782', 'user_id':1}
        assert(validate_customer(customer_field_data=customer_FD))

        customer_FD = {'first_name': 'Murka', 'last_name': 'Paw', 'address':'Israel, Cat-City, Meow-Street, 101/2.', 
        'phone_no':'+40 713 281 837', 'credit_card_no':'4524 7948 2579 0782', 'user_id':1}
        assert(validate_customer(customer_field_data=customer_FD))

        customer_FD = {'first_name': 'Murka', 'last_name': 'Paw', 'address':'Israel, Cat-City, Meow-Street, 101/2.', 
        'phone_no':'++1 350-956-5941', 'credit_card_no':'4524 7948 2579 0782', 'user_id':1}
        assert(validate_customer(customer_field_data=customer_FD)) # The double + gets fixed.

        customer_FD = {'first_name': 'Murka', 'last_name': 'Paw', 'address':'Israel, Cat-City, Meow-Street, 101/2.', 
        'phone_no':'1 350-956-5941', 'credit_card_no':'4524 7948 2579 0782', 'user_id':1}
        assert(validate_customer(customer_field_data=customer_FD)) # + gets added automatically.

        # Wrong uses: ===============================================

        customer_FD = {'first_name': 'M', 'last_name': 'Paw', 'address':'Israel, Cat-City, Meow-Street, 101/2.', 
        'phone_no':'+972 050-101-2101', 'credit_card_no':'4524 7948 2579 0782', 'user_id':1}
        assert(not(validate_customer(customer_field_data=customer_FD)))

        customer_FD = {'first_name': 'MURKAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', 'last_name': 'Paw', 'address':'Israel, Cat-City, Meow-Street, 101/2.', 
        'phone_no':'+972 050-101-2101', 'credit_card_no':'4524 7948 2579 0782', 'user_id':1}
        assert(not(validate_customer(customer_field_data=customer_FD)))

        customer_FD = {'first_name': 'Murka2Cute', 'last_name': 'Paw', 'address':'Israel, Cat-City, Meow-Street, 101/2.', 
        'phone_no':'+972 050-101-2101', 'credit_card_no':'4524 7948 2579 0782', 'user_id':1}
        assert(not(validate_customer(customer_field_data=customer_FD)))

        customer_FD = {'first_name': 'Murka', 'last_name': 'P', 'address':'Israel, Cat-City, Meow-Street, 101/2.', 
        'phone_no':'+972 050-101-2101', 'credit_card_no':'4524 7948 2579 0782', 'user_id':1}
        assert(not(validate_customer(customer_field_data=customer_FD)))

        customer_FD = {'first_name': 'Murka', 'last_name': 'PAWwwwwwwwwwwwwwwwwwwwwwww', 'address':'Israel, Cat-City, Meow-Street, 101/2.', 
        'phone_no':'+972 050-101-2101', 'credit_card_no':'4524 7948 2579 0782', 'user_id':1}
        assert(not(validate_customer(customer_field_data=customer_FD)))

        customer_FD = {'first_name': 'Murka', 'last_name': 'PAWwww@', 'address':'Israel, Cat-City, Meow-Street, 101/2.', 
        'phone_no':'+972 050-101-2101', 'credit_card_no':'4524 7948 2579 0782', 'user_id':1}
        assert(not(validate_customer(customer_field_data=customer_FD)))

        customer_FD = {'first_name': 'Murka', 'last_name': 'Paw', 'address':10001, 
        'phone_no':'+972 050-101-2101', 'credit_card_no':'4524 7948 2579 0782', 'user_id':1}
        assert(not(validate_customer(customer_field_data=customer_FD)))

        customer_FD = {'first_name': 'Murka', 'last_name': 'Paw', 'address':'Israel, Cat.', 
        'phone_no':'+972 050-101-2101', 'credit_card_no':'4524 7948 2579 0782', 'user_id':1}
        assert(not(validate_customer(customer_field_data=customer_FD)))

        customer_FD = {'first_name': 'Murka', 'last_name': 'Paw', 'address':'Israel, Cat-City, MeeeeeeeeeEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEOOOOOOOOOOOOOOOOOOoooooow-Street, 101/2.', 
        'phone_no':'+972 050-101-2101', 'credit_card_no':'4524 7948 2579 0782', 'user_id':1}
        assert(not(validate_customer(customer_field_data=customer_FD)))

        customer_FD = {'first_name': 'Murka', 'last_name': 'Paw', 'address':'Israel, Cat-City, Me@w-Street, 101/2.', 
        'phone_no':'+972 050-101-2101', 'credit_card_no':'4524 7948 2579 0782', 'user_id':1}
        assert(not(validate_customer(customer_field_data=customer_FD)))

        customer_FD = {'first_name': 'Murka', 'last_name': 'Paw', 'address':'Israel, Cat-City, Meow-Street, 101/2.', 
        'phone_no':'+54 9 3865 51-25166666666', 'credit_card_no':'4524 7948 2579 0782', 'user_id':1}
        assert(not(validate_customer(customer_field_data=customer_FD)))

        customer_FD = {'first_name': 'Murka', 'last_name': 'Paw', 'address':'Israel, Cat-City, Meow-Street, 101/2.', 
        'phone_no':'713 281 837', 'credit_card_no':'4524 7948 2579 0782', 'user_id':1}
        assert(not(validate_customer(customer_field_data=customer_FD)))

        customer_FD = {'first_name': 'Murka', 'last_name': 'Paw', 'address':'Israel, Cat-City, Meow-Street, 101/2.', 
        'phone_no':'+972 5', 'credit_card_no':'4524 7948 2579 0782', 'user_id':1}
        assert(not(validate_customer(customer_field_data=customer_FD)))

        customer_FD = {'first_name': 'Murka', 'last_name': 'Paw', 'address':'Israel, Cat-City, Meow-Street, 101/2.', 
        'phone_no':'+972 50-1@1-2101', 'credit_card_no':'4524 7948 2579 0782', 'user_id':1}
        assert(not(validate_customer(customer_field_data=customer_FD)))

        customer_FD = {'first_name': 'Murka', 'last_name': 'Paw', 'address':'Israel, Cat-City, Meow-Street, 101/2.', 
        'phone_no':'+972 50-101-2101', 'credit_card_no':'123 7948', 'user_id':1}
        assert(not(validate_customer(customer_field_data=customer_FD)))

        customer_FD = {'first_name': 'Murka', 'last_name': 'Paw', 'address':'Israel, Cat-City, Meow-Street, 101/2.', 
        'phone_no':'+972 50-1@1-2101', 'credit_card_no':'1234 5678 9101 1121', 'user_id':1}
        assert(not(validate_customer(customer_field_data=customer_FD)))

        customer_FD = {'first_name': 'Murka', 'last_name': 'Paw', 'address':'Israel, Cat-City, Meow-Street, 101/2.', 
        'phone_no':'+972 50-101-2101', 'credit_card_no':'4524 7948 2579 0782', 'user_id':98}
        assert(not(validate_customer(customer_field_data=customer_FD)))


        customer_FD = {'first_name': 'Murka', 'last_name': 'Paw', 'address':'Israel, Cat-City, Meow-Street, 101/2.', 
        'phone_no':'+972 50-101-2101', 'credit_card_no':'4524 7948 2579 0782', 'user_id_id':1}
        DAL.add_instance(some_model=Customers, field_data=customer_FD) #phone number already exists
        customer_FD = {'first_name': 'Murka', 'last_name': 'Paw', 'address':'Israel, Cat-City, Meow-Street, 101/2.', 
        'phone_no':'+972 50-101-2101', 'credit_card_no':'4524 7948 2579 0782', 'user_id':1}
        assert(not(validate_customer(customer_field_data=customer_FD)))

        customer_FD = {'first_name': 'Murka', 'last_name': 'Paw', 'address':'Israel, Cat-City, Meow-Street, 101/2.', 
        'phone_no':'+972 50-101-2102', 'credit_card_no':'4524 7948 2579 0782', 'user_id':1} #credit card already exists
        assert(not(validate_customer(customer_field_data=customer_FD)))

        #test if role name matches 'customer'
        role_FD = {'role_name': 'Administrator'}
        DAL.add_instance(some_model=User_Roles, field_data=role_FD)
        user_FD = {'username':'usemyname123', 'email':'fake@mail123.com', 'password':'A1b2C3d4', 'user_role_id':2}
        DAL.add_instance(some_model=Users, field_data=user_FD)
        customer_FD = {'first_name': 'Murka', 'last_name': 'Paw', 'address':'Israel, Cat-City, Meow-Street, 101/2.', 
        'phone_no':'+972 50-101-2101', 'credit_card_no':'4078-8994-1664-0393', 'user_id':2}
        assert(not(validate_customer(customer_field_data=customer_FD)))


# @pytest.mark.now
class Test_Validate_Administrator(TestCase):

    @pytest.mark.django_db()
    def test_validate_administrator(self):

        # Correct use: ===============================================
        
        role_FD = {'role_name': 'Administrator'}
        DAL.add_instance(some_model=User_Roles, field_data=role_FD)
        user_FD = {'username':'usemyname', 'email':'fake@mail.com', 'password':'A1b2C3d4', 'user_role_id':1}
        DAL.add_instance(some_model=Users, field_data=user_FD)
        admin_FD = {'first_name': 'Murka', 'last_name': 'Paw', 'user_id':1}
        assert(validate_administrator(admin_field_data=admin_FD))

        # Wrong uses: ===============================================

        admin_FD = {'first_name': 'M', 'last_name': 'Paw', 'user_id':1}
        assert(not(validate_administrator(admin_field_data=admin_FD)))

        admin_FD = {'first_name': 'MurkaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaAAAAAAA', 'last_name': 'Paw', 'user_id':1}
        assert(not(validate_administrator(admin_field_data=admin_FD)))

        admin_FD = {'first_name': 'Murka', 'last_name': 'P', 'user_id':1}
        assert(not(validate_administrator(admin_field_data=admin_FD)))

        admin_FD = {'first_name': 'Murka', 'last_name': 'PaaAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAaw', 'user_id':1}
        assert(not(validate_administrator(admin_field_data=admin_FD)))

        admin_FD = {'first_name': 101011, 'last_name': 'Paw', 'user_id':1}
        assert(not(validate_administrator(admin_field_data=admin_FD)))

        admin_FD = {'first_name': 'Murk@', 'last_name': 'Paw', 'user_id':1}
        assert(not(validate_administrator(admin_field_data=admin_FD)))

        admin_FD = {'first_name': 'Murka', 'last_name': '4%w', 'user_id':1}
        assert(not(validate_administrator(admin_field_data=admin_FD)))

        admin_FD = {'first_name': 'Murka', 'last_name': 'Paw', 'user_id':98}
        assert(not(validate_administrator(admin_field_data=admin_FD)))

        #test if role name matches 'Administrator'
        role_FD = {'role_name': 'Customer'}
        DAL.add_instance(some_model=User_Roles, field_data=role_FD)
        user_FD = {'username':'usemyname123', 'email':'fake@mail123.com', 'password':'A1b2C3d4', 'user_role_id':2}
        DAL.add_instance(some_model=Users, field_data=user_FD)
        admin_FD = {'first_name': 'Murka', 'last_name': 'Paw', 'user_id':2}
        assert(not(validate_administrator(admin_field_data=admin_FD)))



# @pytest.mark.now
class Test_Validate_Countries(TestCase):

    @pytest.mark.django_db()
    def test_validate_countries(self):

        # Correct use: ===============================================
        
        flag = SimpleUploadedFile(name='mayama.jpg', content=open("./images2test/mayama.jpg", 'rb').read(), content_type='image/jepg')
        country_FD = {'name': 'Germany', 'flag': flag}
        assert(validate_country(country_field_data=country_FD))

        country_FD = {'name': 'Cat Country', 'flag': flag}
        assert(validate_country(country_field_data=country_FD))

        country_FD = {'name': 'Cat-Country', 'flag': flag}
        assert(validate_country(country_field_data=country_FD))

        flag = SimpleUploadedFile(name='de.png', content=open("./images2test/de.png", 'rb').read(), content_type='image/png')
        country_FD = {'name': 'Germany', 'flag': flag}
        assert(validate_country(country_field_data=country_FD))
        
        flag = SimpleUploadedFile(name='yeah.webp', content=open("./images2test/yeah.webp", 'rb').read(), content_type='image/jpeg')
        country_FD = {'name': 'Germany', 'flag': flag}
        assert(validate_country(country_field_data=country_FD))

        # Wrong uses: ===============================================

        country_FD = {'name': 'Countr33', 'flag': flag}
        assert(not(validate_country(country_field_data=country_FD)))

        country_FD = {'name': 'Cat-C@untry', 'flag': flag}
        assert(not(validate_country(country_field_data=country_FD)))

        flag = SimpleUploadedFile(name='de.png', content=open("./images2test/de.png", 'rb').read(), content_type='image/jpeg')
        country_FD = {'name': 23423, 'flag': flag}
        assert(not(validate_country(country_field_data=country_FD)))

        country_FD = {'name': 'G', 'flag': flag}
        assert((not(validate_country(country_field_data=country_FD))))

        country_FD = {'name': 'Gerrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrmany', 'flag': flag}
        assert((not(validate_country(country_field_data=country_FD))))

        flag = 'meow'
        country_FD = {'name': 'Germany', 'flag': flag}
        assert(not((validate_country(country_field_data=country_FD))))

        flag = 110101011111
        country_FD = {'name': 'Germany', 'flag': flag}
        assert(not((validate_country(country_field_data=country_FD))))



# @pytest.mark.now
class Test_Validate_Airline_Company(TestCase):

    @pytest.mark.django_db()
    def test_validate_airline_company(self):

        # Correct use: ===============================================
        
        role_FD = {'role_name': 'Airline Company'}
        DAL.add_instance(some_model=User_Roles, field_data=role_FD)
        flag = SimpleUploadedFile(name='de.jpg', content=open("./images2test/de.png", 'rb').read(), content_type='image/jpeg')
        country_FD = {'name': 'Germany', 'flag': flag}
        DAL.add_instance(some_model=Countries, field_data=country_FD)
        user_FD = {'username':'usemyname', 'email':'fake@mail.com', 'password':'A1b2C3d4', 'user_role_id':1}
        DAL.add_instance(some_model=Users, field_data=user_FD)
        airline_FD = {'name': 'Murka', 'country_id':1, 'user_id':1}
        assert(validate_airline_company(airline_field_data=airline_FD))

        airline_FD = {'name': 'Purrfect Fluffy-Clouds', 'country_id':1, 'user_id':1}
        assert(validate_airline_company(airline_field_data=airline_FD))

        # Wrong uses: ===============================================

        airline_FD = {'name': 'M', 'country_id':1, 'user_id':1}
        assert(not(validate_airline_company(airline_field_data=airline_FD)))

        airline_FD = {'name': 'MuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuurkaAAAA', 'country_id':1, 'user_id':1}
        assert(not(validate_airline_company(airline_field_data=airline_FD)))

        airline_FD = {'name': 'Murka2fluffy', 'country_id':1, 'user_id':1}
        assert(not(validate_airline_company(airline_field_data=airline_FD)))

        airline_FD = {'name': 'Murk@', 'country_id':1, 'user_id':1}
        assert(not(validate_airline_company(airline_field_data=airline_FD)))

        airline_FD = {'name': 11011, 'country_id':1, 'user_id':1}
        assert(not(validate_airline_company(airline_field_data=airline_FD)))

        airline_FD = {'name': 'Murka', 'country_id':'Yay', 'user_id':1}
        assert(not(validate_airline_company(airline_field_data=airline_FD)))

        airline_FD = {'name': 'Murka', 'country_id':1, 'user_id':'Boo'}
        assert(not(validate_airline_company(airline_field_data=airline_FD)))

        airline_FD = {'name': 'Murka', 'country_id':988, 'user_id':1}
        assert(not(validate_airline_company(airline_field_data=airline_FD)))

        airline_FD = {'name': 'Murka', 'country_id':1, 'user_id':889}
        assert(not(validate_airline_company(airline_field_data=airline_FD)))

        
        airline_FD = {'name': 'Murka', 'country_id_id':1, 'user_id_id':1}
        DAL.add_instance(some_model=Airline_Companies, field_data=airline_FD)
        airline_FD = {'name': 'Murka', 'country_id':1, 'user_id':1}
        assert(not(validate_airline_company(airline_field_data=airline_FD))) # Airline name already exists

        
        role_FD = {'role_name': 'Customer'}
        DAL.add_instance(some_model=User_Roles, field_data=role_FD)
        user_FD = {'username':'usemyname123', 'email':'fake@mail123.com', 'password':'A1b2C3d4', 'user_role_id':2}
        DAL.add_instance(some_model=Users, field_data=user_FD)
        airline_FD = {'name': 'Murka Paw', 'country_id':1, 'user_id':2} # Role name doesn't match 'Airline Company'
        assert(not(validate_airline_company(airline_field_data=airline_FD)))


# @pytest.mark.now
class Test_Validate_Flight(TestCase):

    @pytest.mark.django_db()
    def test_validate_flight(self):

        # Correct use: ===============================================
        
        role_FD = {'role_name': 'Airline Company'}
        DAL.add_instance(some_model=User_Roles, field_data=role_FD)
        flag = SimpleUploadedFile(name='de.jpg', content=open("./images2test/de.png", 'rb').read(), content_type='image/jpeg')
        country_FD = {'name': 'Germany', 'flag': flag}
        DAL.add_instance(some_model=Countries, field_data=country_FD)
        user_FD = {'username':'usemyname', 'email':'fake@mail.com', 'password':'A1b2C3d4', 'user_role_id':1}
        DAL.add_instance(some_model=Users, field_data=user_FD)
        airline_FD = {'name': 'Murka', 'country_id_id':1, 'user_id_id':1}
        DAL.add_instance(some_model=Airline_Companies, field_data=airline_FD)
        flag = SimpleUploadedFile(name='fi.png', content=open("./images2test/fi.png", 'rb').read(), content_type='image/png')
        country_FD = {'name': 'Finland', 'flag': flag}
        DAL.add_instance(some_model=Countries, field_data=country_FD)

        utc = pytz.UTC
        departure = dt.datetime.now()
        landing = departure + dt.timedelta(hours=3)
        flight_FD = {'airline_company_id':1, 'origin_country_id':1, 'destination_country_id':2, 'departure_time':departure,
                     'landing_time':landing, 'remaining_tickets':25}
        assert(validate_flight(flight_field_data=flight_FD))

        departure = dt.datetime.now()
        landing = departure + dt.timedelta(hours=20)
        flight_FD = {'airline_company_id':1, 'origin_country_id':1, 'destination_country_id':2, 'departure_time':departure,
                     'landing_time':landing, 'remaining_tickets':25}
        assert(validate_flight(flight_field_data=flight_FD))

        departure = dt.datetime.now()
        landing = departure + dt.timedelta(minutes=30)
        flight_FD = {'airline_company_id':1, 'origin_country_id':1, 'destination_country_id':2, 'departure_time':departure,
                     'landing_time':landing, 'remaining_tickets':25}
        assert(validate_flight(flight_field_data=flight_FD))

        flight_FD = {'airline_company_id':1, 'origin_country_id':1, 'destination_country_id':2, 'departure_time':departure,
                     'landing_time':landing, 'remaining_tickets':0}
        assert(validate_flight(flight_field_data=flight_FD))

        flight_FD = {'airline_company_id':1, 'origin_country_id':1, 'destination_country_id':2, 'departure_time':departure,
                     'landing_time':landing, 'remaining_tickets':860}
        assert(validate_flight(flight_field_data=flight_FD))

        # Wrong uses: ===============================================

        departure = dt.datetime.now()
        landing = departure + dt.timedelta(minutes=29)
        flight_FD = {'airline_company_id':1, 'origin_country_id':1, 'destination_country_id':2, 'departure_time':departure,
                     'landing_time':landing, 'remaining_tickets':25}
        assert(not(validate_flight(flight_field_data=flight_FD)))

        departure = dt.datetime.now()
        landing = departure + dt.timedelta(minutes=1, hours=20)
        flight_FD = {'airline_company_id':1, 'origin_country_id':1, 'destination_country_id':2, 'departure_time':departure,
                     'landing_time':landing, 'remaining_tickets':25}
        assert(not(validate_flight(flight_field_data=flight_FD)))

        departure = dt.datetime.now()
        landing = departure + dt.timedelta(hours=3)
        flight_FD = {'airline_company_id':1, 'origin_country_id':1, 'destination_country_id':1, 'departure_time':departure,
                     'landing_time':landing, 'remaining_tickets':25}
        assert(not(validate_flight(flight_field_data=flight_FD))) # destination is the same as origin

        flight_FD = {'airline_company_id':998, 'origin_country_id':1, 'destination_country_id':2, 'departure_time':departure,
                     'landing_time':landing, 'remaining_tickets':25}
        assert(not(validate_flight(flight_field_data=flight_FD)))

        flight_FD = {'airline_company_id':'idNot', 'origin_country_id':1, 'destination_country_id':2, 'departure_time':departure,
                     'landing_time':landing, 'remaining_tickets':25}
        assert(not(validate_flight(flight_field_data=flight_FD)))

        flight_FD = {'airline_company_id':1, 'origin_country_id':998, 'destination_country_id':2, 'departure_time':departure,
                     'landing_time':landing, 'remaining_tickets':25}
        assert(not(validate_flight(flight_field_data=flight_FD)))

        flight_FD = {'airline_company_id':1, 'origin_country_id':'idNot', 'destination_country_id':2, 'departure_time':departure,
                     'landing_time':landing, 'remaining_tickets':25}
        assert(not(validate_flight(flight_field_data=flight_FD)))

        flight_FD = {'airline_company_id':1, 'origin_country_id':1, 'destination_country_id':998, 'departure_time':departure,
                     'landing_time':landing, 'remaining_tickets':25}
        assert(not(validate_flight(flight_field_data=flight_FD)))

        flight_FD = {'airline_company_id':1, 'origin_country_id':1, 'destination_country_id':'idNot', 'departure_time':departure,
                     'landing_time':landing, 'remaining_tickets':25}
        assert(not(validate_flight(flight_field_data=flight_FD)))

        
        flight_FD = {'airline_company_id':1, 'origin_country_id':1, 'destination_country_id':2, 'departure_time':departure,
                     'landing_time':landing, 'remaining_tickets':-1}
        assert(not(validate_flight(flight_field_data=flight_FD)))

        flight_FD = {'airline_company_id':1, 'origin_country_id':1, 'destination_country_id':2, 'departure_time':departure,
                     'landing_time':landing, 'remaining_tickets':861}
        assert(not(validate_flight(flight_field_data=flight_FD)))

        flight_FD = {'airline_company_id':1, 'origin_country_id':1, 'destination_country_id':2, 'departure_time':departure,
                     'landing_time':landing, 'remaining_tickets':0.1}
        assert(not(validate_flight(flight_field_data=flight_FD)))

        flight_FD = {'airline_company_id':1, 'origin_country_id':1, 'destination_country_id':2, 'departure_time':departure,
                     'landing_time':landing, 'remaining_tickets':'yes'}
        assert(not(validate_flight(flight_field_data=flight_FD)))

    
# @pytest.mark.now
class Test_Validate_Ticket(TestCase):

    @pytest.mark.django_db()
    def test_validate_ticket(self):

        # Correct use: ===============================================
        
        role_FD = {'role_name': 'Airline Company'}
        DAL.add_instance(some_model=User_Roles, field_data=role_FD)
        flag = SimpleUploadedFile(name='de.jpg', content=open("./images2test/de.png", 'rb').read(), content_type='image/jpeg')
        country_FD = {'name': 'Germany', 'flag': flag}
        DAL.add_instance(some_model=Countries, field_data=country_FD)
        user_FD = {'username':'usemyname', 'email':'fake@mail.com', 'password':'A1b2C3d4', 'user_role_id':1}
        DAL.add_instance(some_model=Users, field_data=user_FD)
        airline_FD = {'name': 'Murka', 'country_id_id':1, 'user_id_id':1}
        DAL.add_instance(some_model=Airline_Companies, field_data=airline_FD)
        flag = SimpleUploadedFile(name='fi.png', content=open("./images2test/fi.png", 'rb').read(), content_type='image/png')
        country_FD = {'name': 'Finland', 'flag': flag}
        DAL.add_instance(some_model=Countries, field_data=country_FD)
        utc = pytz.UTC
        departure = dt.datetime.now()
        landing = departure + dt.timedelta(hours=3)
        flight_FD = {'airline_company_id_id':1, 'origin_country_id_id':1, 'destination_country_id_id':2, 'departure_time':departure,
                     'landing_time':landing, 'remaining_tickets':25}
        DAL.add_instance(some_model=Flights, field_data=flight_FD)
        
        role_FD = {'role_name': 'Customer'}
        DAL.add_instance(some_model=User_Roles, field_data=role_FD)
        user_FD = {'username':'usemyname2', 'email':'fake2@mail.com', 'password':'A1b2C3d4', 'user_role_id':2}
        DAL.add_instance(some_model=Users, field_data=user_FD)
        customer_FD = {'first_name': 'Murka', 'last_name': 'Paw', 'address':'Israel, Cat-City, Meow-Street, 101/2.', 
        'phone_no':'+972 50-101-2101', 'credit_card_no':'4524 7948 2579 0782', 'user_id_id':1}
        DAL.add_instance(some_model=Customers, field_data=customer_FD)

        # (^ IK, IK, a horror to look at. But unfortunately it's far too late now to regret not making any data set up fixtures. #Never again.)

        ticket_FD = {'flight_id': 1, 'customer_id':1}
        assert(validate_ticket(ticket_field_data=ticket_FD))

        # Wrong uses: ===============================================

        ticket_FD = {'flight_id': 'lastoneyay', 'customer_id':1}
        assert(not(validate_ticket(ticket_field_data=ticket_FD)))

        ticket_FD = {'flight_id': 99, 'customer_id':1}
        assert(not(validate_ticket(ticket_field_data=ticket_FD)))

        ticket_FD = {'flight_id': 1, 'customer_id':'boredomhellimout'}
        assert(not(validate_ticket(ticket_field_data=ticket_FD)))

        ticket_FD = {'flight_id': 1, 'customer_id':994}
        assert(not(validate_ticket(ticket_field_data=ticket_FD)))

        ticket_FD = {'flight_id_id': 1, 'customer_id_id':1}
        DAL.add_instance(some_model=Tickets, field_data=ticket_FD)
        ticket_FD = {'flight_id': 1, 'customer_id':1}
        assert(not(validate_ticket(ticket_field_data=ticket_FD))) # The customer&flight id combo must be unique

# @pytest.mark.now
@pytest.mark.skip
class Test_DAL_Val_Add_User(TestCase):

    @pytest.mark.django_db()
    def test_DAL_add_instance(self):
        # Correct uses: ===============================================
        role_FD = {'role_name': 'Administrator'}
        DAL.add_instance(some_model=User_Roles, field_data=role_FD)
        role = User_Roles.objects.get(role_name='Administrator')
        assert(role)

        user_FD = {'username':'usemyname', 'email':'fake@mail.com', 'password':'A1b2C3d4', 'user_role_id':role.id}
        val_add_user(user_field_data=user_FD)
        user = Users.objects.get(username='usemyname')
        assert(user)

        thumbnail = SimpleUploadedFile(name='test_image.jpg', content=open("./images2test/yeah.webp", 'rb').read(), content_type='image/jpeg')
        user_FD = {'username':'usemynametoo', 'email':'fake2@mail.com', 'password':'A1b2C3d4', 'user_role_id':role.id, 'thumbnail':thumbnail}
        val_add_user(user_field_data=user_FD)
        user2 = Users.objects.get(username='usemynametoo')
        assert(user2)