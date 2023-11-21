from django.test import TestCase
import pytest
from airline_reservation_system.utiles import *


# @pytest.mark.now
@pytest.mark.skip
class Test_Val_Add_User(TestCase):

    @pytest.mark.django_db()
    def test_val_add_user(self):
        # Correct uses: ===============================================
        if not(populate_user_roles()):
            print("'populate_user_roles' failed. Can't run this test.")
            assert(False)

        thumbnail = SimpleUploadedFile(name='test_image.jpg', content=open("./web-design/static/UA1.jpg", 'rb').read(), content_type='image/jpg')
        user_FD = {'username':'Cat', 'email':'fake@meow.purr', 'password':'Murka1234', 'user_role_id':1, 'thumbnail':thumbnail}
        assert(val_add_user(user_field_data=user_FD))
        
        thumbnail = SimpleUploadedFile(name='test_image.jpg', content=open("./web-design/static/UAC2.jpg", 'rb').read(), content_type='image/jpg')
        user_FD = {'username':'Purrfect', 'email':'fluffy@clouds.yay', 'password':'Fly1234', 'user_role_id':2, 'thumbnail':thumbnail}
        assert(val_add_user(user_field_data=user_FD))
        
        thumbnail = SimpleUploadedFile(name='test_image.jpg', content=open("./web-design/static/UC3.jpg", 'rb').read(), content_type='image/jpg')
        user_FD = {'username':'Ace', 'email':'cyclops@pew.why', 'password':'Change1234', 'user_role_id':3, 'thumbnail':thumbnail}
        assert(val_add_user(user_field_data=user_FD))

        thumbnail = SimpleUploadedFile(name='test_image.jpg', content=open("./web-design/static/UA4.jpg", 'rb').read(), content_type='image/jpg')
        user_FD = {'username':'HighlyMethodical', 'email':'johnh@me.com', 'password':'tzQbE7uUw', 'user_role_id':1, 'thumbnail':thumbnail}
        assert(val_add_user(user_field_data=user_FD))
        
        thumbnail = SimpleUploadedFile(name='test_image.jpg', content=open("./web-design/static/UAC5.webp", 'rb').read(), content_type='image/webp')
        user_FD = {'username':'snobby3penguin', 'email':'monopole@verizon.net', 'password':'GbhYY8a96', 'user_role_id':2, 'thumbnail':thumbnail}
        assert(val_add_user(user_field_data=user_FD))
        
        thumbnail = SimpleUploadedFile(name='test_image.jpg', content=open("./web-design/static/UC6.jpg", 'rb').read(), content_type='image/jpg')
        user_FD = {'username':'giddyloser', 'email':'alias@optonline.net', 'password':'D4eeZV6RX', 'user_role_id':3, 'thumbnail':thumbnail}
        assert(val_add_user(user_field_data=user_FD))
        
        user_FD = {'username':'unknown2U', 'email':'shh@secretline.com', 'password':'thumbnail2Check', 'user_role_id':3}
        assert(val_add_user(user_field_data=user_FD))
    

# @pytest.mark.now
@pytest.mark.skip
class Test_Populate_All(TestCase):

    @pytest.mark.django_db()
    def test_populate_all(self):
        
        assert(populate_all())
        ticket = Tickets.objects.get(id=1)
        assert(ticket)


# pytest .\airline_reservation_system\test_utiles.py::Test_Randomly_Populate_Users
# @pytest.mark.skip
class Test_Randomly_Populate_Users(TestCase):

    @pytest.mark.django_db()
    def test_randomly_populate_users(self):
        if not(populate_user_roles()):
            print("'populate_user_roles' failed. Can't run this test.")
            assert(False)

        assert(randomly_populate_users(amount=3, any_role=2))



from io import StringIO
from django.core import management

# @pytest.mark.now
@pytest.mark.skip
class Test_For_Missing_Migrations(TestCase):

    @pytest.mark.django_db()
    def test_for_missing_migrations(self):
        output = StringIO()
        management.call_command("makemigrations", no_input=True, dry_run=True, stdout=output)
        assert output.getvalue().strip() == "No changes detected", (
            "There are missing migrations:\n %s" % output.getvalue()
        )