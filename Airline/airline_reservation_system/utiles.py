from django.core.validators import validate_email
import re
from airline_reservation_system.models import *
from airline_reservation_system.dal import *
from airline_reservation_system.validators import *
from airline_reservation_system.validators import validate_id, validate_instance_type, get_role_by_user
from PIL import Image
from phonenumber_field.validators import validate_international_phonenumber
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import request
import base64
import random
from randimage import get_random_image
import random_address
import randominfo
from random_username.generate import generate_username
import logging 
logger = logging.getLogger("pick.me") 


def update_role_session(request:request ,user_id:int):
    """
    Stores the current logged user's role name in session.
    Upon failure returns False and an error msg str,
    upon success returns True and the role name str.
    """
    role_name = get_role_by_user(user_id=user_id)
    if role_name==False:
        err_msg = f"Failed to get a user's ({user_id = }) role name."
        logger.error(err_msg)
        return False, err_msg
    request.session['user_role'] = role_name
    info_msg = f"Successfully updated the session's role name value. request.session['user_role'] = {role_name}."
    logger.info(info_msg)
    return True, role_name


def get_user_id_from_session(request:request):
    """
    Upon failure returns an error msg str,
    upon success returns a user_id int.
    """
    try:    
        user_id = request.session['user_id']
    except Exception as e:
        err_msg = f"Failed to get 'user_id' from session. Error: {e}"
        logger.error(err_msg)
        return err_msg
    if (type(user_id)!=int):
        err_msg = f"Failed to get 'user_id'."
        logger.error(err_msg)
        return err_msg
    info_msg = f"Successfully got 'user_id' = {user_id}, from session."
    logger.info(info_msg)
    return user_id

def initialize_api_counter():
    """
    Will be used to limit the "randomly_populate_all_api" to 3 times in total, regardless of server reloads.
    This is done so that no one could fill the database with too much fake data.
    """
    counter, created = APICounter.objects.get_or_create(pk=1)
    if created:
        counter.count = 0
        counter.save()

def prepare_profile(profile:str):
    profile = str(profile)
    logger.info('profile path = ', profile)
    try:
        path = profile
        split_path = path.split("Airline\\", 1)
        if len(split_path) > 1:
            new_path = split_path[-1]
        else:
            new_path = path
        new_path = new_path.replace("\\", "/")
        logger.info('NEW profile path = ', new_path)
        with open(new_path, 'rb') as image_file:
            image_data = image_file.read()
            encoded_image = base64.b64encode(image_data).decode('utf-8')
            return encoded_image

    except Exception as e:
        with open("web-design/static/no_profile.jpg", 'rb') as image_file:
            image_data = image_file.read()
            encoded_image = base64.b64encode(image_data).decode('utf-8')
            return encoded_image
        

# VALIDATE & RETURN: =====================================
# (Used to validate serializers. Returns error messages when validation fails, and a dictionary when it succeeds.) 

def validate_and_return_userFD(user_field_data:dict):
    """
    validates and adds a user.
    returns false if validation fails and vise versa.
    Send raw unencrypted password only.
    """
    unique_bypass = False
    partial = False
    addition = False
    username = ''
    must_have_fields = ['username', 'password', 'email', 'thumbnail', 'user_role_id']
    keys = list(user_field_data.keys())
    if (type(user_field_data) != dict):
        error_msg = f"Bad input. Failed to validate a user.'user_field_data' must be a dictionary."
        logger.error(error_msg)
        return False, error_msg
    data = user_field_data

    if ('partial' in data.keys()): 
        partial = data['partial']

    if not partial:
        goal = len(must_have_fields)
        test = [key for key in (sorted(keys)) if key in must_have_fields]
        if ( len(test) != goal ):
            error_msg = f"Please make sure that user_field_data's keys contain all the following field names of {Users}. Here are those fields: {must_have_fields}, and here are your keys: {keys}."
            logger.error(error_msg)
            return False, error_msg

    if ('id' in data.keys()): # RTS: Must be done first or else username and email won't get their bypass flag prepared in time for the unique check.
        user_id = int(data['id'])
        if not(validate_id(some_model=Users, id=user_id)):
                error_msg = f"Bad input. Failed to validate a user. id = {user_id} can't be found."
                logger.error(error_msg)
                return False, error_msg
        unique_bypass = True

    for key, val in data.items():

        if key=='username':
            username = val
            if not((type(val) == str) and (20 >= len(val) >= 3)):
                error_msg = f"Bad input. Failed to validate a user.'username'(={username}) must be a string with a minimum of 3 characters and a maximum of 20 characters in length."
                logger.error(error_msg)
                return False, error_msg
            if not(re.match("^[a-zA-Z0-9_-]*$", val)): 
                error_msg = f"Bad input. Failed to validate a user.'username'(={username}) can only contain English letters[a-z, A-Z], numbers[0-9], '-' and '_'."
                logger.error(error_msg)
                return False, error_msg
            if ( (Users.objects.filter(username=username).exists()) and (unique_bypass==False) ):
                error_msg = f"Bad input. Failed to validate a user.'username'(={username}) is already taken."
                logger.error(error_msg)
                return False, error_msg
            
        if key=='password':
            val = str(val)

            valid_chars = re.match("^[a-zA-Z0-9]*$", val)
            good_len = bool(20 >= len(val) >= 6)
            all_num = bool(val.isnumeric())
            all_alpha = bool(val.isalpha())

            not_valid = bool((not valid_chars) or not(good_len) or all_alpha or all_num)
            encrypted_pass = bool((val == "pass") and (partial==True))

            if(not_valid and (not encrypted_pass)): 
                error_msg = f"Bad input. Failed to validate a user. 'password'(={val}) must be a string with a minimum of 6 characters and a maximum of 20 characters in length. It must contain English letters and numbers, but not be consisted of only numbers or only letters."
                logger.error(error_msg) # DW, I won't be logging this sensitive password info if this insufficient system was used for real
                return False, error_msg
            
        if key=='email':
            try:
                validate_email(val)
            except Exception as e:
                error_msg = f"Bad input. Failed to validate a user. Check your 'email' address(={val}), details: {e}"
                logger.error(error_msg)
                return False, error_msg
            if ( Users.objects.filter(email=val).exists()  and (unique_bypass==False) ):
                error_msg = f"Bad input. Failed to validate a user.'email'(={val}) is already taken. Perhaps you can login instead?"
                logger.error(error_msg)
                return False, error_msg

        if key=='user_role_id':
            if not(validate_id(some_model=User_Roles, id=val)):
                error_msg = f"Bad input. Failed to validate a user. 'user_role' id(={val}) can't be found."
                logger.error(error_msg)
                return False, error_msg
            if (val==1):
                addition = {}
                addition['is_superuser'] = val
                addition['is_staff'] = val
            else: # In case the user was an administrator before the role change.
                addition = {}
                addition['is_superuser'] = 0
                addition['is_staff'] = 0
            
        if key=='thumbnail':
            try:
                im = Image.open(val)
                im.verify()
                im.close()
                im = Image.open(val) 
                im.transpose(Image.FLIP_LEFT_RIGHT)
                im.close()
            except: 
                error_msg = f"Bad input. Failed to validate a user(={username}). Thumbnail image is corrupted or in an invalid format. Acceptable formats: ['.jpg'/'.jpeg'/'.webp']."
                logger.error(error_msg)
                return False, error_msg

    if ('thumbnail' not in keys ): # if no thumbnail was uploaded, it inserts a default image.
        data['thumbnail'] = SimpleUploadedFile(name='test_image.jpg', content=open("./web-design/static/no_profile.jpg", 'rb').read(), content_type='image/jpg')

    if addition:
        data.update(addition)

    info_msg = f"Successfully validated and returned a user field data dictionary. 'username' = '{username}'."
    logger.info(info_msg)
    return True, data


def validate_and_return_customerFD(customer_field_data:dict):
    """
    validates and returns a customer.
    returns false if the process fails and vise versa.
    Don't include id.
    """
    
    unique_bypass = False
    partial = False
    addition = False
    phone_no = ''
    credit_card = 0    
    must_have_fields = ['first_name', 'last_name', 'address', 'phone_no', 'credit_card_no', 'user_id_id']

    keys = list(customer_field_data.keys())
    if (type(customer_field_data) != dict):
        error_msg = f"Bad input. Failed to validate a customer.'customer_field_data' must be a dictionary."
        logger.error(error_msg)
        return False, error_msg
    data = customer_field_data

    if ('partial' in data.keys()): 
        partial = data['partial']

    if not partial:
        goal = len(must_have_fields)
        test = [key for key in (sorted(keys)) if key in must_have_fields]
        if ( len(test) != goal ):
            error_msg = f"Please make sure that customer_field_data's keys contain all the following field names of {Customers}. Here are those fields: {must_have_fields}, and here are your keys: {keys}."
            logger.error(error_msg)
            return False, error_msg

    if ('id' in data.keys()): 
        customer_id = int(data['id'])
        if not(validate_id(some_model=Customers, id=customer_id)):
            error_msg = f"Bad input. Failed to validate a customer. id = {customer_id} can't be found."
            logger.error(error_msg)
            return False, error_msg
        unique_bypass = True

        
    for key, val in data.items():

        if (key=='first_name' or key=='last_name'):
            if not((type(val) == str) and (20 >= len(val) >= 2)):
                error_msg = f"Bad input. Failed to validate a customer.'{key}'(={val}) must be a string with a minimum of 2 characters and a maximum of 20 characters in length."
                logger.error(error_msg)
                return False, error_msg
            if not(val.isalpha()): 
                error_msg = f"Bad input. Failed to validate a customer.'{key}'(={val}) can only contain English letters[a-z, A-Z]."
                logger.error(error_msg)
                return False, error_msg
        
        if key=='address':
            if not((type(val) == str) and (150 >= len(val) >= 15)):
                error_msg = f"Bad input. Failed to validate a customer.'{key}'(={val}) must be a string with a minimum of 15 characters and a maximum of 150 characters in length."
                logger.error(error_msg)
                return False, error_msg
            raw_val = r'{}'.format(val)
            if not(re.match("^[a-zA-Z0-9.,-/\\s]*$", raw_val)): 
                error_msg = f"Bad input. Failed to validate a customer.'{key}'(={val}) can only contain English letters[a-z, A-Z], numbers, white spaces, and the following symbols:[ ' - , . / ]."
                logger.error(error_msg)
                return False, error_msg

        if key=='phone_no':
            val = str(val)
            raw_val = r'{}'.format(val)
            raw_val = re.sub(r'[^0-9]', "", raw_val)
            phone_no = '+'+raw_val
            try: 
                validate_international_phonenumber(phone_no)
            except Exception as e:
                error_msg = f"Bad input. Failed to validate a customer. '{key}'(={raw_val}) isn't valid. error: {e}"
                logger.error(error_msg)
                return False, error_msg
            if ( (Customers.objects.filter(phone_no=val).exists()) and (unique_bypass==False)):
                error_msg = f"Bad input. Failed to validate a customer.'phone_no'(={val}) is already in use by another customer."
                logger.error(error_msg)
                return False, error_msg
    
        if key=='credit_card_no':
            val = str(val)
            raw_val = r'{}'.format(val)
            raw_val = re.sub(r'[^0-9]+', "", raw_val)
            credit_card = raw_val
            if not(re.match("^(?:4[0-9]{12}(?:[0-9]{3})?|[25][1-7][0-9]{14}|6(?:011|5[0-9][0-9])[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|(?:2131|1800|35\\d{3})\\d{11})$", raw_val)):
                error_msg = f"Bad input. Failed to validate a customer. '{key}'(={raw_val}) isn't valid. Valid credit cards: Visa, MasterCard, American Express, Diners Club, Discover, and JCB."
                logger.error(error_msg)
                return False, error_msg
            if ( (Customers.objects.filter(credit_card_no=val).exists()) and (unique_bypass==False)):
                error_msg = f"Bad input. Failed to validate a customer.'credit_card_no'(={val}) is already in use by another customer."
                logger.error(error_msg)
                return False, error_msg
            
        if key=='user_id_id':
            if not(validate_id(some_model=Users, id=val)):
                error_msg = f"Bad input. Failed to validate a customer. 'user_id' id(={val}) can't be found."
                logger.error(error_msg)
                return False, error_msg
            role_name = get_role_by_user(user_id=val)
            if (role_name != 'Customer'):
                error_msg = f"Bad input. Failed to validate a customer. The user role of 'user_id_id' id(={val}) must be 'Customer', not '{role_name}'."
                logger.error(error_msg)
                return False, error_msg
            if ( (Customers.objects.filter(user_id_id=val).exists()) and (unique_bypass==False)):
                error_msg = f"Bad input. Failed to validate a customer.'user_id_id'(={val}) is already in use by another customer."
                logger.error(error_msg)
                return False, error_msg
    
    customer_field_data['phone_no'] = phone_no
    customer_field_data['credit_card_no'] = credit_card

    info_msg = f"Successfully validated and returned a customer field data dictionary. 'phone_no' = '{phone_no}'."
    logger.info(info_msg)
    return True, data


def validate_and_return_adminFD(admin_field_data:dict):
    """
    validates and returns an administrator.
    returns false if validation fails and vise versa.
    Don't include id.
    """
    unique_bypass = False
    partial = False
    addition = False
    user_id = 0
    must_have_fields = ['first_name', 'last_name', 'user_id_id']

    keys = list(admin_field_data.keys())
    if (type(admin_field_data) != dict):
        error_msg = f"Bad input. Failed to validate an administrator. 'admin_field_data' must be a dictionary."
        logger.error(error_msg)
        return False, error_msg
    data = admin_field_data

    if ('partial' in data.keys()): 
        partial = data['partial']

    if not partial:
        goal = len(must_have_fields)
        test = [key for key in (sorted(keys)) if key in must_have_fields]
        if ( len(test) != goal ):
            error_msg = f"Please make sure that admin_field_data's keys contain all the following field names of {Administrators}. Here are those fields: {must_have_fields}, and here are your keys: {keys}."
            logger.error(error_msg)
            return False, error_msg

    if ('id' in data.keys()): 
        admin_id = int(data['id'])
        if not(validate_id(some_model=Administrators, id=admin_id)):
                error_msg = f"Bad input. Failed to validate an administrator. id = {admin_id} can't be found."
                logger.error(error_msg)
                return False, error_msg
        unique_bypass = True

    
    for key, val in data.items():

        if (key=='first_name' or key=='last_name'):
            if not((type(val) == str) and (20 >= len(val) >= 2)):
                error_msg = f"Bad input. Failed to validate an administrator.'{key}'(={val}) must be a string with a minimum of 2 characters and a maximum of 20 characters in length."
                logger.error(error_msg)
                return False, error_msg
            if not(val.isalpha()): 
                error_msg = f"Bad input. Failed to validate an administrator.'{key}'(={val}) can only contain English letters[a-z, A-Z]."
                logger.error(error_msg)
                return False, error_msg
        
        if key=='user_id_id':
            user_id = val
            if not(validate_id(some_model=Users, id=val)):
                error_msg = f"Bad input. Failed to validate an administrator. 'user_id' id(={val}) can't be found."
                logger.error(error_msg)
                return False, error_msg
            role_name = get_role_by_user(user_id=val)
            if (role_name != 'Administrator'):
                error_msg = f"Bad input. Failed to validate an administrator. The user role of 'user_id' id(={val}) must be 'Administrator', not '{role_name}'."
                logger.error(error_msg)
                return False, error_msg
            if ( (Administrators.objects.filter(user_id_id=val).exists()) and (unique_bypass==False)):
                error_msg = f"Bad input. Failed to validate an administrator.'user_id_id'(={val}) is already in use by another administrator."
                logger.error(error_msg)
                return False, error_msg
    
    info_msg = f"Successfully validated and returned an administrator. 'user_id' = '{user_id}'.)"
    logger.info(info_msg)
    return True, data


def validate_and_return_airlineFD(airline_field_data:dict):
    """
    validates and returns an airline company.
    returns false if validation fails and vise versa.
    """
    unique_bypass = False
    partial = False
    addition = False
    user_id = 0
    must_have_fields =  ['name', 'country_id_id', 'user_id_id']

    keys = list(airline_field_data.keys())
    if (type(airline_field_data) != dict):
        error_msg = f"Bad input. Failed to validate an airline company. 'airline_field_data' must be a dictionary."
        logger.error(error_msg)
        return False, error_msg
    data = airline_field_data

    if ('partial' in data.keys()): 
        partial = data['partial']

    if not partial:
        goal = len(must_have_fields)
        test = [key for key in (sorted(keys)) if key in must_have_fields]
        if ( len(test) != goal ):
            error_msg = f"Please make sure that airline_field_data's keys contain all the following field names of {Airline_Companies}. Here are those fields: {must_have_fields}, and here are your keys: {keys}."
            logger.error(error_msg)
            return False, error_msg

    if ('id' in data.keys()): 
        airline_id = int(data['id'])
        if not(validate_id(some_model=Airline_Companies, id=airline_id)):
            error_msg = f"Bad input. Failed to validate an airline company. id = {airline_id} can't be found."
            logger.error(error_msg)
            return False, error_msg
        unique_bypass = True
        logger.info(f"hey?, {unique_bypass = }.")
    
    logger.info(f"In validate airline, {unique_bypass = }.")

    for key, val in data.items():

        if key=='name':
            name = val
            if not((type(val) == str) and (30 >= len(val) >= 2)):
                error_msg = f"Bad input. Failed to validate an airline company. '{key}'(={val}) must be a string with a minimum of 2 characters and a maximum of 30 characters in length."
                logger.error(error_msg)
                return False, error_msg
            if not(re.match("^[a-zA-Z- ]*$", val)): 
                error_msg = f"Bad input. Failed to validate an airline company. '{key}'(={val}) can contain only English letters[a-z, A-Z], '-' and whitespaces."
                logger.error(error_msg)
                return False, error_msg
            if ( (Airline_Companies.objects.filter(name=val).exists()) and (unique_bypass==False)):
                logger.info(f"222 In validate airline, {unique_bypass = }.")
                error_msg = f"Bad input. Failed to validate an airline company. 'name'(={val}) already exists in the database."
                logger.error(error_msg)
                return False, error_msg
            
        if key=='country_id_id':
            if not(validate_id(some_model=Countries, id=val)):
                error_msg = f"Bad input. Failed to validate an airline company. 'country_id' id(={val}) can't be found."
                logger.error(error_msg)
                return False, error_msg
        
        if key=='user_id_id':
            user_id = val
            if not(validate_id(some_model=Users, id=val)):
                error_msg = f"Bad input. Failed to validate an airline company. 'user_id' id(={val}) can't be found."
                logger.error(error_msg)
                return False, error_msg
            role_name = get_role_by_user(user_id=val)
            if (role_name != 'Airline Company'):
                error_msg = f"Bad input. Failed to validate an airline company. The user role of 'user_id' id(={val}) must be 'Airline Company', not '{role_name}'."
                logger.error(error_msg)
                return False, error_msg
            if ( (Airline_Companies.objects.filter(user_id_id=val).exists()) and (unique_bypass==False)):
                error_msg = f"Bad input. Failed to validate an airline company.'user_id_id'(={val}) is already in use by another airline company."
                logger.error(error_msg)
                return False, error_msg
        
    info_msg = f"Successfully validated and returned an airline company, 'name' = '{name}'. 'user_id' = '{user_id}'.)"
    logger.info(info_msg)
    return True, data


def validate_and_return_flightFD(flight_field_data:dict):
    """
    validates and returns a flight.
    returns false if validation fails and vise versa.
    Don't include id.
    """
    partial = False
    addition = False
    origin = 0
    departure_time = ''
    must_have_fields =  ['airline_company_id_id', 'origin_country_id_id', 'destination_country_id_id', 'departure_time', 'landing_time', 'remaining_tickets']

    keys = list(flight_field_data.keys())
    if (type(flight_field_data) != dict):
        error_msg = f"Bad input. Failed to validate a flight. 'flight_field_data' must be a dictionary."
        logger.error(error_msg)
        return False, error_msg
    data = flight_field_data

    if ('partial' in data.keys()): 
        partial = data['partial']

    if not partial:
        goal = len(must_have_fields)
        test = [key for key in (sorted(keys)) if key in must_have_fields]
        if ( len(test) != goal ):
            error_msg = f"Please make sure that flight_field_data's keys contain all the following field names of {Flights}. Here are those fields: {must_have_fields}, and here are your keys: {keys}."
            logger.error(error_msg)
            return False, error_msg

    if ('id' in data.keys()): 
        flight_id = int(data['id'])
        if not(validate_id(some_model=Flights, id=flight_id)):
                error_msg = f"Bad input. Failed to validate a flight. id = {flight_id} can't be found."
                logger.error(error_msg)
                return False, error_msg
    
    print(f"{data = }")
    for key, val in data.items():

        if key=='airline_company_id_id':
            airline = val
            if not(validate_id(some_model=Airline_Companies, id=val)):
                error_msg = f"Bad input. Failed to validate a flight. 'airline_company_id' id(={val}) can't be found."
                logger.error(error_msg)
                return False, error_msg
            
        if key=='origin_country_id_id':
            origin = val
            if not(validate_id(some_model=Countries, id=val)):
                error_msg = f"Bad input. Failed to validate a flight. 'origin_country_id' id(={val}) can't be found."
                logger.error(error_msg)
                return False, error_msg
        
        if key=='destination_country_id_id':
            if (not(validate_id(some_model=Countries, id=val))):
                error_msg = f"Bad input. Failed to validate a flight. 'destination_country_id' id(={val}) can't be found."
                logger.error(error_msg)
                return False, error_msg
            if origin == val:
                error_msg = f"Bad input. Failed to validate a flight. 'destination_country_id' id(={val}) can't be the same as origin_country_id."
                logger.error(error_msg)
                return False, error_msg
        
        if key=='departure_time':
            departure_time = val
            if not(isinstance(val, dt.datetime)):
                error_msg = f"Bad input. Failed to validate a flight. 'departure_time'(={val}) is not a datetime object."
                logger.error(error_msg)
                return False, error_msg
            val_str = val.strftime('%Y-%m-%d')
            if not(dt.date.fromisoformat(val_str)):
                error_msg = f"Bad input. Failed to validate a flight. 'departure_time'(={val}) is in an incorrect data format, the format should be 'YYYY-MM-DD'."
                logger.error(error_msg)
                return False, error_msg
            # print(val, 'type: ', type(val))
            start = dt.datetime(year=1909, month=11, day=16)
            now_dt = datetime.now().replace(second=0, microsecond=0)
            too_far = now_dt + dt.timedelta(days=365)
            # print(f'1-thisssssssss: ({dt.datetime.now()} <= {val} <= {too_far}) ', ' = ',(dt.datetime.now() <= val <= too_far) )# decided to let users input old flights too (flights which includes times before now), so this isn't relevant anymore. But I'll leave this here in case I change my mind later.
            if ((val < start) or ( val >= too_far) ): # On November 16, 1909, the world's first airline, DELAG (Deutsche Luftschiffahrts-Aktiengesellschaft or German Airship Company) was established.
                error_msg = f"Bad input. Failed to validate a flight. 'departure_time'(={val}) should be after 1909/11/16 and before a year from now which is {too_far}."
                logger.error(error_msg)
                return False, error_msg
        
        if key=='landing_time':
            landing_time = val
            if not(isinstance(val, dt.datetime)):
                error_msg = f"Bad input. Failed to validate a flight. 'landing_time'(={val}) is not a datetime object."
                logger.error(error_msg)
                return False, error_msg
            val_str = val.strftime('%Y-%m-%d')
            if not(dt.date.fromisoformat(val_str)):
                error_msg = f"Bad input. Failed to validate a flight. 'landing_time'(={val}) is in an incorrect data format, the format should be 'YYYY-MM-DD'."
                logger.error(error_msg)
                return False, error_msg
            too_far = departure_time + dt.timedelta(hours=20)
            too_short = departure_time + dt.timedelta(minutes=30)
            print(f'2-thisssssssss: ({too_short} <= {val} <= {too_far}) ', ' = ',(too_short <= val <= too_far) )
            if ((val < start) or not(too_short <= val <= too_far) ): 
                error_msg = f"Bad input. Failed to validate a flight. 'landing_time'(={val}), is invalid because the duration of a flight can not be shorter than half an hour, or longer than 20 hours. So the landing time should be after {too_short} and before {too_far}."
                logger.error(error_msg)
                return False, error_msg
        
        if key=='remaining_tickets':
            if not(type(val) is int):
                error_msg = f"Bad input. Failed to validate a flight. 'remaining_tickets'(={val}) must be an integer."
                logger.error(error_msg)
                return False, error_msg
            if not(0 <= val <= 860):
                error_msg = f"Bad input. Failed to validate a flight. 'remaining_tickets'(={val}) can not be a negative number, or bigger than 860."
                logger.error(error_msg)
                return False, error_msg
    
    info_msg = f"Successfully validated and returned a flight. 'airline_company_id' = '{airline}', 'departure_time' = '{departure_time}', 'landing_time' = '{landing_time}'.)"
    logger.info(info_msg)
    return True, data

def validate_and_return_ticketFD(ticket_field_data:dict):
    """
    validates and returns a ticket.
    returns false if validation fails and vise versa.
    Don't include id.
    """
    unique_bypass = False
    partial = False
    addition = False
    flight_id = 0
    customer_id = 0
    must_have_fields = ['flight_id_id', 'customer_id_id']

    keys = list(ticket_field_data.keys())
    if (type(ticket_field_data) != dict):
        error_msg = f"Bad input. Failed to validate a ticket. 'ticket_field_data' must be a dictionary."
        logger.error(error_msg)
        return False, error_msg
    data = ticket_field_data

    if ('partial' in data.keys()): 
        partial = data['partial']

    if not partial:
        goal = len(must_have_fields)
        test = [key for key in (sorted(keys)) if key in must_have_fields]
        if ( len(test) != goal ):
            error_msg = f"Please make sure that ticket_field_data's keys contain all the following field names of {Tickets}. Here are those fields: {must_have_fields}, and here are your keys: {keys}."
            logger.error(error_msg)
            return False, error_msg

    if ('id' in data.keys()): 
        ticket_id = int(data['id'])
        if not(validate_id(some_model=Tickets, id=ticket_id)):
                error_msg = f"Bad input. Failed to validate a ticket. id = {ticket_id} can't be found."
                logger.error(error_msg)
                return False, error_msg
        unique_bypass = True

    
    for key, val in data.items():
    
        if key=='flight_id_id':
            flight_id = val
            if not(validate_id(some_model=Flights, id=val)):
                error_msg = f"Bad input. Failed to validate a ticket. 'flight_id' id(={val}) can't be found."
                logger.error(error_msg)
                return False, error_msg
            try:
                flight = Flights.objects.get(id=flight_id)
                remaining_tickets = flight.remaining_tickets
                departure = flight.departure_time
                now_dt = datetime.now().replace(second=0, microsecond=0)
                time_diff = departure - now_dt
                too_late = bool(time_diff < timedelta(hours=1))
                if (remaining_tickets<1):
                    error_msg = f"Failed to validate a ticket. The tickets of the flight with id = {flight_id}, were already all sold out."
                    logger.error(error_msg)
                    return False, error_msg
                if too_late:
                    error_msg = f"Failed to validate a ticket. The ticket of the flight with id = {flight_id}, can't be sold because there's already less than an hour left before the flight's departure. It's too late to buy it now. (flight's departure: {departure}, now: {now_dt})"
                    logger.error(error_msg)
                    return False, error_msg

            except Exception as e:
                error_msg = f"Failed to validate a ticket. The tickets of the flight with id = {flight_id}, were already all sold out. Error: {e}"
                logger.error(error_msg)
                return False, error_msg
            
        if key=='customer_id_id':
            customer_id = val
            if not(validate_id(some_model=Customers, id=val)):
                error_msg = f"Bad input. Failed to validate a ticket. 'customer_id' id(={val}) can't be found."
                logger.error(error_msg)
                return False, error_msg
        
        try:
            if ((Tickets.objects.filter(Q(flight_id_id=flight_id), Q(customer_id_id=customer_id)).exists()) and (unique_bypass==False)):
                error_msg = f"Bad input. Failed to validate a ticket. A ticket with the given data: 'customer_id' = {customer_id}, 'flight_id' = {flight_id}, already exists in the database. Or in other words, you already own this ticket. You can't buy the same ticket twice."
                logger.error(error_msg)
                return False, error_msg
            continue
        except Exception as e:
            error_msg = f"Bad input. Failed to validate a ticket. Ticket database search failed. error: {e}"
            logger.error(error_msg)
            return False, error_msg
        

    info_msg = f"Successfully validated and returned a ticket. 'customer_id' = {customer_id}, 'flight_id' = {flight_id}.)"
    logger.info(info_msg)
    return True, data


"""
The following part combines validation and add/update DAL operations into one function.
This is needed because some of my validators change and edit the values of the data dictionary that they receive.
They do so in order to fit the DAL's field formats, or to set default data when optional data is emitted (when it can't be done in the models). 
"""
# VALIDATE & ADD: =====================================
def val_add_user(user_field_data:dict):
    """
    Validates and adds a user.
    Returns the new user object if validation succeeds, and returns False otherwise.
    Send raw unencrypted password only.
    """

    username = ''
    bad_fields = ['last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'groups', 'user_permissions', 'thumbnail', 'id', 'first_name', 'last_name', 'user_role']
    fields = [field.name for field in Users._meta.get_fields(include_parents=False, include_hidden=False) if (field.name not in bad_fields)]
    fields.append('user_role_id')
    keys = list(user_field_data.keys())
    if (type(user_field_data) != dict):
        error_msg = f"Bad input. Failed to validate a user.'user_field_data' must be a dictionary."
        logger.error(error_msg)
        return False
    data = user_field_data
    optional = list(fields) #https://stackoverflow.com/questions/29785084/changing-one-list-unexpectedly-changes-another-too
    optional.append('thumbnail')
    if ( ( sorted(fields)!=sorted(keys) ) and ( sorted(optional)!=sorted(keys) ) ):
        error_msg = f"Please make sure that user_field_data's keys match the field names of {Users}. Here are those fields: {fields}, and here are your keys: {keys}."
        logger.error(error_msg)
        return False
    
    if ( sorted(fields)==sorted(keys) ): # if no thumbnail was uploaded, it inserts a default image.
        data['thumbnail'] = SimpleUploadedFile(name='test_image.jpg', content=open("./web-design/static/no_profile.jpg", 'rb').read(), content_type='image/jpg')

    for key, val in data.items():

        if key=='username':
            username = val
            if not((type(val) == str) and (20 >= len(val) >= 3)):
                error_msg = f"Bad input. Failed to validate a user.'username'(={username}) must be a string with a minimum of 3 characters and a maximum of 20 characters in length."
                logger.error(error_msg)
                return False
            if not(re.match("^[a-zA-Z0-9_-]*$", val)): 
                error_msg = f"Bad input. Failed to validate a user.'username'(={username}) can only contain English letters[a-z, A-Z], numbers[0-9], '-' and '_'."
                logger.error(error_msg)
                return False
            if ( Users.objects.filter(username=username).exists() ):
                error_msg = f"Bad input. Failed to validate a user.'username'(={username}) is already taken."
                logger.error(error_msg)
                return False
            
        if key=='password':
            val = str(val)
            if not(re.match("^[a-zA-Z0-9]*$", val) and (20 >= len(val) >= 6) and (data['username'] != val) and (not(val.isnumeric())) and (not(val.isalpha())) ):
                error_msg = f"Bad input. Failed to validate a user. 'password'(={val}) must be a string with a minimum of 6 characters and a maximum of 20 characters in length. It must contain English letters and numbers, but not be consisted of only numbers or only letters. It must also be different from your username."
                logger.error(error_msg) # DW, I won't be logging this sensitive password info if this insufficient system was used for real
                return False
            
        if key=='email':
            try:
                validate_email(val)
            except Exception as e:
                error_msg = f"Bad input. Failed to validate a user. Check your 'email' address(={val}), details: {e}"
                logger.error(error_msg)
                return False
            if ( Users.objects.filter(email=val).exists() ):
                error_msg = f"Bad input. Failed to validate a user.'email'(={val}) is already taken. Perhaps you can login instead?"
                logger.error(error_msg)
                return False

        if key=='user_role_id':
            if not(validate_id(some_model=User_Roles, id=val)):
                error_msg = f"Bad input. Failed to validate a user. 'user_role' id(={val}) can't be found."
                logger.error(error_msg)
                return False
            
        if key=='thumbnail':
            try:
                im = Image.open(val)
                im.verify()
                im.close()
                im = Image.open(val) 
                im.transpose(Image.FLIP_LEFT_RIGHT)
                im.close()
            except: 
                error_msg = f"Bad input. Failed to validate a user(={username}). Thumbnail image is corrupted or in an invalid format. Acceptable formats: ['.jpg'/'.jpeg'/'.webp']."
                logger.error(error_msg)
                return False

    info_msg = f"Successfully validated a user. 'username' = '{username}'."
    logger.info(info_msg)
    user = DAL.add_instance(some_model=Users, field_data=data)
    if (type(user) == str):
            error_msg = f"Failed to add a user. 'username' = '{username}'."
            logger.error(error_msg)
            return False
    info_msg = f"Successfully validated and added a user. 'username' = '{username}'."
    logger.info(info_msg)
    return user


def val_add_customer(customer_field_data:dict):
    """
    validates and adds a customer.
    returns false if the process fails and vise versa.
    Don't include id.
    """
    phone_no = ''
    credit_card = 0
    bad_fields = ['id', 'user_id']
    fields = [field.name for field in Customers._meta.get_fields() if (field.name not in bad_fields)]
    fields.append('user_id_id')
    keys = list(customer_field_data.keys())
    if (type(customer_field_data) != dict):
        error_msg = f"Bad input. Failed to validate a customer.'customer_field_data' must be a dictionary."
        logger.error(error_msg)
        return False
    data = customer_field_data
    if sorted(fields)!=sorted(keys):
        error_msg = f"Please make sure that customer_field_data's keys match the field names of {Customers}. Here are those fields: {fields}, and here are your keys: {keys}."
        logger.error(error_msg)
        return False
        
    for key, val in data.items():

        if (key=='first_name' or key=='last_name'):
            if not((type(val) == str) and (20 >= len(val) >= 2)):
                error_msg = f"Bad input. Failed to validate a customer.'{key}'(={val}) must be a string with a minimum of 2 characters and a maximum of 20 characters in length."
                logger.error(error_msg)
                return False
            if not(val.isalpha()): 
                error_msg = f"Bad input. Failed to validate a customer.'{key}'(={val}) can only contain English letters[a-z, A-Z]."
                logger.error(error_msg)
                return False
        
        if key=='address':
            if not((type(val) == str) and (150 >= len(val) >= 15)):
                error_msg = f"Bad input. Failed to validate a customer.'{key}'(={val}) must be a string with a minimum of 15 characters and a maximum of 150 characters in length."
                logger.error(error_msg)
                return False
            raw_val = r'{}'.format(val)
            if not(re.match("^[a-zA-Z0-9.,-/\\s]*$", raw_val)): 
                error_msg = f"Bad input. Failed to validate a customer.'{key}'(={val}) can only contain English letters[a-z, A-Z], numbers, white spaces, and the following symbols:[ ' - , . / ]."
                logger.error(error_msg)
                return False

        if key=='phone_no':
            val = str(val)
            raw_val = r'{}'.format(val)
            raw_val = re.sub(r'[^0-9]', "", raw_val)
            phone_no = '+'+raw_val
            try: 
                validate_international_phonenumber(phone_no)
            except Exception as e:
                error_msg = f"Bad input. Failed to validate a customer. '{key}'(={raw_val}) isn't valid. error: {e}"
                logger.error(error_msg)
                return False
    
        if key=='credit_card_no':
            val = str(val)
            raw_val = r'{}'.format(val)
            raw_val = re.sub(r'[^0-9]+', "", raw_val)
            credit_card = raw_val
            if not(re.match("^(?:4[0-9]{12}(?:[0-9]{3})?|[25][1-7][0-9]{14}|6(?:011|5[0-9][0-9])[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|(?:2131|1800|35\\d{3})\\d{11})$", raw_val)):
                error_msg = f"Bad input. Failed to validate a customer. '{key}'(={raw_val}) isn't valid. Valid credit cards: Visa, MasterCard, American Express, Diners Club, Discover, and JCB."
                logger.error(error_msg)
                return False
            if ( Customers.objects.filter(credit_card_no=val).exists() ):
                error_msg = f"Bad input. Failed to validate a customer.'credit_card_no'(={val}) is already in use by another customer."
                logger.error(error_msg)
                return False
            
        if key=='user_id_id':
            if not(validate_id(some_model=Users, id=val)):
                error_msg = f"Bad input. Failed to validate a customer. 'user_id' id(={val}) can't be found."
                logger.error(error_msg)
                return False
            role_name = get_role_by_user(user_id=val)
            if (role_name != 'Customer'):
                error_msg = f"Bad input. Failed to validate a customer. The user role of 'user_id_id' id(={val}) must be 'Customer', not '{role_name}'."
                logger.error(error_msg)
                return False
    
    customer_field_data['phone_no'] = phone_no
    customer_field_data['credit_card_no'] = credit_card

    info_msg = f"Successfully validate a customer. 'phone_no' = '{phone_no}'."
    logger.info(info_msg)
    if (type(DAL.add_instance(some_model=Customers, field_data=customer_field_data)) == str):
            error_msg = f"Failed to add a customer. 'phone_no' = '{phone_no}'."
            logger.error(error_msg)
            return False
    info_msg = f"Successfully validated and added a customer. 'phone_no' = '{phone_no}'."
    logger.info(info_msg)
    return True


# VALIDATE & UPDATE: =====================================

def val_up_customer(customer_field_data:dict, instance:Customers):
    """
    validates and updates a customer.
    returns false if the process fails and vise versa.
    You must include id.
    """
    id = 0
    if not(validate_instance_type(some_model=Customers, instance=instance)):
        error_msg = f"Failed to validate an instance before update. Bad input. 'instance' is not an instance of Customers."
        logger.error(error_msg)
        return False
    
    id = DAL.get_id_from_instance(instance=instance)
    if not(type(id) == int):
        error_msg = f"Failed to validate an instance before update. Bad input. Couldn't get the id of 'instance'."
        logger.error(error_msg)
        return False
    
    phone_no = ''
    credit_card = 0

    bad_fields = ['id', 'user_id']
    fields = [field.name for field in Customers._meta.get_fields() if (field.name not in bad_fields)]
    fields.append('user_id_id')
    keys = list(customer_field_data.keys())
    if (type(customer_field_data) != dict):
        error_msg = f"Bad input. Failed to validate a customer.'customer_field_data' must be a dictionary."
        logger.error(error_msg)
        return False
    data = customer_field_data
    if sorted(fields)!=sorted(keys):
        error_msg = f"Please make sure that customer_field_data's keys match the field names of {Customers}. Here are those fields: {fields}, and here are your keys: {keys}."
        logger.error(error_msg)
        return False
        
    for key, val in data.items():

        if (key=='first_name' or key=='last_name'):
            if not((type(val) == str) and (20 >= len(val) >= 2)):
                error_msg = f"Bad input. Failed to validate a customer.'{key}'(={val}) must be a string with a minimum of 2 characters and a maximum of 20 characters in length."
                logger.error(error_msg)
                return False
            if not(val.isalpha()): 
                error_msg = f"Bad input. Failed to validate a customer.'{key}'(={val}) can only contain English letters[a-z, A-Z]."
                logger.error(error_msg)
                return False
        
        if key=='address':
            if not((type(val) == str) and (150 >= len(val) >= 15)):
                error_msg = f"Bad input. Failed to validate a customer.'{key}'(={val}) must be a string with a minimum of 15 characters and a maximum of 150 characters in length."
                logger.error(error_msg)
                return False
            raw_val = r'{}'.format(val)
            if not(re.match("^[a-zA-Z0-9.,-/\\s]*$", raw_val)): 
                error_msg = f"Bad input. Failed to validate a customer.'{key}'(={val}) can only contain English letters[a-z, A-Z], numbers, white spaces, and the following symbols:[ ' - , . / ]."
                logger.error(error_msg)
                return False

        if key=='phone_no':
            val = str(val)
            raw_val = r'{}'.format(val)
            raw_val = re.sub(r'[^0-9]', "", raw_val)
            phone_no = '+'+raw_val
            try: 
                validate_international_phonenumber(phone_no)
            except Exception as e:
                error_msg = f"Bad input. Failed to validate a customer. '{key}'(={raw_val}) isn't valid. error: {e}"
                logger.error(error_msg)
                return False
    
        if key=='credit_card_no':
            val = str(val)
            raw_val = r'{}'.format(val)
            raw_val = re.sub(r'[^0-9]+', "", raw_val)
            credit_card = raw_val
            if not(re.match("^(?:4[0-9]{12}(?:[0-9]{3})?|[25][1-7][0-9]{14}|6(?:011|5[0-9][0-9])[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|(?:2131|1800|35\\d{3})\\d{11})$", raw_val)):
                error_msg = f"Bad input. Failed to validate a customer. '{key}'(={raw_val}) isn't valid. Valid credit cards: Visa, MasterCard, American Express, Diners Club, Discover, and JCB."
                logger.error(error_msg)
                return False
            if ( Customers.objects.filter(credit_card_no=val).exists() ):
                error_msg = f"Bad input. Failed to validate a customer.'credit_card_no'(={val}) is already in use by another customer."
                logger.error(error_msg)
                return False
            
        if key=='user_id_id':
            if not(validate_id(some_model=Users, id=val)):
                error_msg = f"Bad input. Failed to validate a customer. 'user_id' id(={val}) can't be found."
                logger.error(error_msg)
                return False
            role_name = get_role_by_user(user_id=val)
            if (role_name != 'Customer'):
                error_msg = f"Bad input. Failed to validate a customer. The user role of 'user_id_id' id(={val}) must be 'Customer', not '{role_name}'."
                logger.error(error_msg)
                return False
    
    customer_field_data['phone_no'] = phone_no
    customer_field_data['credit_card_no'] = credit_card

    info_msg = f"Successfully validate a customer. 'phone_no' = '{phone_no}'.)"
    logger.info(info_msg)
    
    if (type(DAL.update_instance(some_model=Customers, instance=instance, field_data=customer_field_data)) == str):
            error_msg = f"Failed to update a customer. 'phone_no' = '{phone_no}'."
            logger.error(error_msg)
            return False
    
    info_msg = f"Successfully validated and updated a customer. 'phone_no' = '{phone_no}'.)"
    logger.info(info_msg)
    return True
   

# SYSTEM INIT: =====================================

"""
ARS data init function. (Can't be placed in dal due to circular import) 
"""

def populate_all():
    """
    Fills in the tables with some initial data
    """

    # NECESSARY!! =========================
     
    # Countries & User_Roles
    if not(populate_user_roles() and populate_countries()):
        return False

    # Users
    thumbnail = SimpleUploadedFile(name='test_image.jpg', content=open("./web-design/static/UA1.jpg", 'rb').read(), content_type='image/jpg')
    user_FD = {'username':'Cat', 'email':'fake@meow.purr', 'password':'Murka1234', 'user_role_id':1, 'thumbnail':thumbnail}
    if not(val_add_user(user_field_data=user_FD)):
        return False
    
    thumbnail = SimpleUploadedFile(name='test_image.jpg', content=open("./web-design/static/UAC2.jpg", 'rb').read(), content_type='image/jpg')
    user_FD = {'username':'Purrfect', 'email':'fluffy@clouds.yay', 'password':'Fly1234', 'user_role_id':2, 'thumbnail':thumbnail}
    if not(val_add_user(user_field_data=user_FD)):
        return False
    
    thumbnail = SimpleUploadedFile(name='test_image.jpg', content=open("./web-design/static/UC3.jpg", 'rb').read(), content_type='image/jpg')
    user_FD = {'username':'Ace', 'email':'cyclops@pew.why', 'password':'Change1234', 'user_role_id':3, 'thumbnail':thumbnail}
    if not(val_add_user(user_field_data=user_FD)):
        return False
    
    # Customers
    customer_FD = {'first_name':'Bernard', 'last_name':'Wiseman', 'address':'Germany, Zeon, spacecol.78.', 
                    'phone_no':'+49 163 09083378', 'credit_card_no':'4929493965436444', 'user_id_id':3}
    if not(val_add_customer(customer_field_data=customer_FD)):
        return False
    
    # Administrator
    admin_FD = {'first_name':'Dev', 'last_name':'Zero', 'user_id_id':1}
    if (DAL.add_instance(some_model=Administrators, field_data=admin_FD) == str):
        return False
    
    # Airline_Companies
    airline_FD = {'name':'Purrfect Fluffy Clouds', 'country_id_id':1, 'user_id_id':2}
    if (DAL.add_instance(some_model=Airline_Companies, field_data=airline_FD) == str):
        return False

    # Flights
    departure = dt.datetime.now().replace(second=0, microsecond=0)
    landing = departure + timedelta(hours=3)
    flight_FD = {'airline_company_id_id':1, 'origin_country_id_id':1, 'destination_country_id_id':2, 'departure_time':departure, 'landing_time':landing, 'remaining_tickets':1}
    if (DAL.add_instance(some_model=Flights, field_data=flight_FD) == str):
        return False
    
    for i in range(15):
        flight_FD = randomly_generate_flight(airline_id=1)
        while(validate_b4_add(some_model=Flights, field_data=flight_FD)==False):
            flight_FD = randomly_generate_flight(airline_id=1)
        flight_FD['airline_company_id_id'] = flight_FD.pop('airline_company_id')
        flight_FD['origin_country_id_id'] = flight_FD.pop('origin_country_id')
        flight_FD['destination_country_id_id'] = flight_FD.pop('destination_country_id')
        DAL.add_instance(some_model=Flights, field_data=flight_FD)
    
    # Tickets
    tickets_FD = {'flight_id_id':1, 'customer_id_id':1}
    if (DAL.add_instance(some_model=Tickets, field_data=tickets_FD) == str):
        return False


    # ADDITIONAL =========================

    # Users
    thumbnail = SimpleUploadedFile(name='test_image.jpg', content=open("./web-design/static/UA4.jpg", 'rb').read(), content_type='image/jpg')
    user_FD = {'username':'HighlyMethodical', 'email':'johnh@me.com', 'password':'tzQbE7uUw', 'user_role_id':1, 'thumbnail':thumbnail}
    if not(val_add_user(user_field_data=user_FD)):
        return False
    
    thumbnail = SimpleUploadedFile(name='test_image.jpg', content=open("./web-design/static/UAC5.webp", 'rb').read(), content_type='image/webp')
    user_FD = {'username':'snobby3penguin', 'email':'monopole@verizon.net', 'password':'GbhYY8a96', 'user_role_id':2, 'thumbnail':thumbnail}
    if not(val_add_user(user_field_data=user_FD)):
        return False
    thumbnail = SimpleUploadedFile(name='test_image.jpg', content=open("./web-design/static/UC6.jpg", 'rb').read(), content_type='image/jpg')
    user_FD = {'username':'giddyloser', 'email':'alias@optonline.net', 'password':'D4eeZV6RX', 'user_role_id':3, 'thumbnail':thumbnail}
    if not(val_add_user(user_field_data=user_FD)):
        return False
    
    user_FD = {'username':'unknown2U', 'email':'shh@secretline.com', 'password':'thumbnail2Check', 'user_role_id':3}
    if not(val_add_user(user_field_data=user_FD)):
        return False
    
    # Customers
    customer_FD = {'first_name':'Ally', 'last_name':'Duffy', 'address':'7244 Elm Dr.Myrtle Beach, SC 29577', 
                    'phone_no':'+1 541-788-0806', 'credit_card_no':'5400507946480497', 'user_id_id':6}
    if not(val_add_customer(customer_field_data=customer_FD)):
        return False
    
    # Administrator
    admin_FD = {'first_name':'Johnh', 'last_name':'Cline', 'user_id_id':4}
    if (DAL.add_instance(some_model=Administrators, field_data=admin_FD) == str):
        return False
    
    # Airline_Companies
    airline_FD = {'name':'Breezy-Chain', 'country_id_id':31, 'user_id_id':5}
    if (DAL.add_instance(some_model=Airline_Companies, field_data=airline_FD) == str):
        return False

    # Flights
    departure = dt.datetime.now().replace(second=0, microsecond=0)
    landing = departure + timedelta(hours=3)
    flight_FD = {'airline_company_id_id':2, 'origin_country_id_id':58, 'destination_country_id_id':36, 'departure_time':departure, 'landing_time':landing, 'remaining_tickets':2}
    if (DAL.add_instance(some_model=Flights, field_data=flight_FD) == str):
        return False
    
    departure = dt.datetime.now().replace(second=0, microsecond=0) - dt.timedelta(days=1)
    landing = departure + timedelta(hours=3)
    flight_FD = {'airline_company_id_id':2, 'origin_country_id_id':58, 'destination_country_id_id':36, 'departure_time':departure, 'landing_time':landing, 'remaining_tickets':2}
    if (DAL.add_instance(some_model=Flights, field_data=flight_FD) == str):
        return False
    
    for i in range(15):
        flight_FD = randomly_generate_flight(airline_id=1)
        while(validate_b4_add(some_model=Flights, field_data=flight_FD)==False):
            flight_FD = randomly_generate_flight(airline_id=1)
        flight_FD['airline_company_id_id'] = flight_FD.pop('airline_company_id')
        flight_FD['origin_country_id_id'] = flight_FD.pop('origin_country_id')
        flight_FD['destination_country_id_id'] = flight_FD.pop('destination_country_id')
        DAL.add_instance(some_model=Flights, field_data=flight_FD)
    
    # Tickets
    tickets_FD = {'flight_id_id':2, 'customer_id_id':2}
    if (DAL.add_instance(some_model=Tickets, field_data=tickets_FD) == str):
        return False
 
    return True


def get_email(username:str):
	domains = ["gmail", "yahoo", "hotmail", "express", "yandex", "nexus", "online", "omega", "institute", "finance", "company", "corporation", "community"]
	extensions = ['com', 'in', 'jp', 'us', 'uk', 'org', 'edu', 'au', 'de', 'co', 'me', 'biz', 'dev', 'ngo', 'site', 'xyz', 'zero', 'tech']
	choice = random.Random().choice
	num = random.randint(0,1000)
	dmn = '@' + choice(domains)
	ext = '.' + choice(extensions)
	
	return username+str(num)+dmn+ext

def randomly_generate_admin(user_id:int):
    """
    Generates random data for an 'Administrator' instance and returns it in a dictionary.
    """
    first_name = randominfo.get_first_name()
    last_name = randominfo.get_last_name()
    admin_FD = {'first_name': first_name, 'last_name': last_name, 'user_id':user_id}
    return admin_FD
    
def randomly_generate_airline(user_id:int):
    """
    Generates random data for an 'Airline_Companies' instance and returns it in a dictionary.
    """
    airline_names = [
        "AeroJet",
        "SkyLink",
        "StarWings",
        "FlyNova",
        "AirVoyage",
        "SwiftAir",
        "JetGlobe",
        "AquaAir",
        "AirHorizon",
        "BlueSky",
        "AirWave",
        "CloudLine",
        "SilverJet",
        "WingStar",
        "AlphaAir",
        "SkyQuest",
        "AviaExpress",
        "FlightMasters",
        "AirVista",
        "AeroLinx",
        "SkyTrails",
        "FlyRise",
        "JetStream",
        "CosmoWings",
        "VoyageAir",
        "AirQuest",
        "StarJet",
        "AirSail",
        "AeroSwift",
        "Skyway",
        "AirVortex",
        "NovaWings",
        "FlyHaven",
        "JetLink",
        "BlueLine",
        "AeroWave",
        "CloudJet",
        "SilverSky",
        "WingSpan",
        "AlphaJet",
        "SkyGlide",
        "AviaStar",
        "FlightPoint",
        "AirVantage",
        "AeroLink",
        "SkyScape",
        "FlyQuest",
        "JetRise",
        "CosmoLinx",
        "VoyageJet",
        "AirScape",
        "StarGlide",
        "AirSurge",
        "AeroNova",
        "SkySail",
        "FlySwift",
        "JetHaven",
        "BlueLink",
        "AeroStream",
        "CloudSpan",
        "SilverQuest",
        "WingHaven",
        "AlphaLine",
        "SkyPoint",
        "AviaVista",
        "FlightWave",
        "AirMasters",
        "AeroVoyage",
        "SkyTrails",
        "FlyRise",
        "JetStream",
        "CosmoWings",
        "VoyageAir",
        "AirQuest",
        "StarJet",
        "AirSail",
        "AeroSwift",
        "Skyway",
        "AirVortex",
        "NovaWings",
        "FlyHaven",
        "JetLink",
        "BlueLine",
        "AeroWave",
        "CloudJet",
        "SilverSky",
        "WingSpan",
        "AlphaJet",
        "SkyGlide",
        "AviaStar",
        "FlightPoint",
        "AirVantage",
        "AeroLink",
        "SkyScape",
        "FlyQuest",
        "JetRise",
        "CosmoLinx",
        "VoyageJet",
        "AirScape",
        "StarGlide",
        "AirSurge",
        "AeroNova",
        "SkySail",
        "FlySwift",
        "JetHaven",
        "BlueLink",
        "AeroStream",
        "CloudSpan",
        "SilverQuest",
        "WingHaven",
        "AlphaLine",
        "SkyPoint",
        "AviaVista",
        "FlightWave",
        "AirMasters"
    ]

    spaceless_name = random.choice(airline_names)
    name = re.sub(r'(.)([A-Z][a-z]+)', r'\1 \2', spaceless_name).strip() # Adds a space before the capital letters, excluding the first one.
    country_id = random.randint(1, 249)
    airline_FD = {'name':name, 'country_id':country_id, 'user_id':user_id}
    return airline_FD

def random_datetime(start: datetime, end: datetime):
    """
    Generates a random datetime within a given range.
    """
    total_seconds = (end - start).total_seconds()
    minutes = int(total_seconds / 60)
    minutes_divisible_by_5 = random.randint(0, minutes // 5) * 5

    return start + timedelta(minutes=minutes_divisible_by_5)

def generate_landing_datetime(departure_time:datetime):
    """
    Generates a landing datetime from a given departure datetime, under the following conditions:
    1) The landing should be at least more than 35 minutes ahead of the first datetime, but no more than 15 hours ahead of it. 
    2) The seconds must always be at zero. 
    3) The minutes should always be evenly divisible by 5.
    """

    # Define the minimum and maximum time differences for landing datetime
    min_diff = timedelta(minutes=35)
    max_diff = timedelta(hours=15)

    # Generate a random time difference within the defined range
    time_diff = random.randint(min_diff.seconds, max_diff.seconds)
    landing_time = departure_time + timedelta(seconds=time_diff)

    # Round the minutes to the nearest multiple of 5
    landing_time = landing_time.replace(minute=(landing_time.minute // 5) * 5)

    # Set the seconds to zero
    landing_time = landing_time.replace(second=0)

    return landing_time

def generate_flight_schedule():
    """
    Returns a dictionary which contains a hypothetical flight's VALID departure and landing datetimes. 
    They will be randomly chosen and generated from a time range between now, and a year from now.
    """

    # Get the current datetime
    now = datetime.now()

    # Define the time range for the first datetime (from now to a year from now)
    start_time = now
    end_time = now + timedelta(days=365)

    # Generate the first datetime within the time range
    departure_time = random_datetime(start_time, end_time)

    # Generate the second datetime based on the conditions
    landing_time = generate_landing_datetime(departure_time)

    departure_time = departure_time.replace(second=0, microsecond=0)
    landing_time = landing_time.replace(second=0, microsecond=0)

    # Create and return the flight schedule dictionary
    flight_schedule = {'departure': departure_time, 'landing': landing_time}
    return flight_schedule

def generate_diff_ints(start:int, end:int):
    """
    Generates two different integers from the same chosen range.
    """

    # Generate the first random integer
    first_integer = random.randint(start, end)

    # Generate the second random integer until it is different from the first
    second_integer = random.randint(start, end)
    while second_integer == first_integer:
        second_integer = random.randint(start, end)

    return first_integer, second_integer

def randomly_generate_flight(airline_id:int):
    """
    Generates random data for a 'Flights' instance and returns it in a dictionary.
    """
    flight_schedule = generate_flight_schedule()
    departure = flight_schedule["departure"]
    landing = flight_schedule["landing"]
    origin, destination = generate_diff_ints(1,249)
    flight_FD = {'airline_company_id':airline_id, 'origin_country_id':origin, 'destination_country_id':destination, 'departure_time':departure, 'landing_time':landing, 'remaining_tickets':random.randint(0, 860)}
    return flight_FD

def generate_fake_credit_card_number():
    while True:
        # Generate a random credit card number
        credit_card_number = generate_random_credit_card_number()

        # Validate the credit card number
        if validate_credit_card_number(credit_card_number):
            return credit_card_number

def generate_random_credit_card_number():
    # Generate a random 16-digit credit card number
    credit_card_number = '4' + ''.join(random.choice('0123456789') for _ in range(15))
    return credit_card_number

def validate_credit_card_number(credit_card_number):
    # Remove non-digit characters from the credit card number
    raw_val = re.sub(r'[^0-9]+', "", credit_card_number)

    # Check if the credit card number matches the given regular expression pattern
    pattern = "^(?:4[0-9]{12}(?:[0-9]{3})?|[25][1-7][0-9]{14}|6(?:011|5[0-9][0-9])[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|(?:2131|1800|35\\d{3})\\d{11})$"
    if not re.match(pattern, raw_val):
        return False

    return True

def generate_fake_phone_number():
    while True:
        # Generate a random phone number
        phone_number = generate_random_phone_number()

        # Validate the phone number
        if validate_phone_number(phone_number):
            return phone_number

def generate_random_phone_number():
    # Generate a random 10-digit phone number
    phone_number = ''.join(random.choice('0123456789') for _ in range(10))
    return phone_number

def validate_phone_number(phone_number):
    # Remove non-digit characters from the phone number
    raw_val = re.sub(r'[^0-9]', "", phone_number)

    # Add '+' at the beginning of the phone number
    phone_no = '+' + raw_val

    try:
        # Validate the international phone number
        validate_international_phonenumber(phone_no)
    except Exception as e:
        return False

    return True

def randomly_generate_customer(user_id:int):
    """
    Generates random data for a 'Customers' instance and returns it in a dictionary.
    """
    firstN = randominfo.get_first_name(gender=None)
    lastN = randominfo.get_last_name()
    dict_address = random_address.real_random_address()
    address = dict_address['state'] + ', ' + dict_address['city'] + ', ' + dict_address['address1'] + '.'
    phone = generate_fake_phone_number()
    card = generate_fake_credit_card_number()
    customer_FD = {'first_name': firstN, 'last_name': lastN, 'address':address, 
                    'phone_no':phone, 'credit_card_no':card, 'user_id':user_id}
    return customer_FD
    
def randomly_populate_users(amount:int, any_role:int):
    """
    Adds x "amount" of randomly generated users to the database. 
    Returns a dictionary of the new users's data upon success, False otherwise.
    If "any_role" is 0, only Customer users will get added.
    If "any_role" is 1, all roles at random can get added.
    If "any_role" is 2, AMOUNT will get OVERWRITTEN to 10, and all roles will get added with tactful proportions: 7/10 customers, 2/10 airlines, 1/10 administrator.
    * Example of a successful scenario's output:  {1: {'username': 'cynicalSheep0', 'password': 'erRj49', 'user_role': 3, 'user_id': 1}, 2: {'username': 'mildVenison7', 'password': 'Iozz41', 'user_role': 2, 'user_id': 2}}
    """
    try:
        amount = int(amount)
        any_role = int(any_role)
        if amount==0:
            amount = 1
        if any_role==2:
            amount = 10
        user_cnt = 0
        users = {}
        for i in range(0,amount):
            if any_role==0:
                role = 3
            elif any_role==1:
                role = random.randint(1,3)
            elif any_role==2:
                number = i + 1
                if number % 10 == 0:
                    role = 1
                elif number % 8 == 0 or number % 9 == 0:
                    role = 2
                # elif any(number % n == 0 for n in range(1, 8)):
                else: 
                    role = 3
            else:
                raise ValueError
            role = int(role)
            username = generate_username()
            username = str(username[0])
            email = get_email(username=username)
            password = randominfo.random_password(length=6, special_chars=False)
            img_size = (450,450)
            profile_pic = get_random_image(img_size) 
            profile_pic = Image.fromarray((profile_pic * 255).astype('uint8')).save('./web-design/random_gen/pic.jpg')
            profile_pic = SimpleUploadedFile(name='test_image.jpg', content=open('./web-design/random_gen/pic.jpg', 'rb').read(), content_type='image/jpg')
            user_FD = {'username':username, 'email':email, 'password':password, 'user_role_id':role, 'thumbnail':profile_pic}
            user = val_add_user(user_field_data=user_FD)
            if not(user):
                raise Exception
            user_cnt += 1
            users[user_cnt] = {"username":username, "password":password, "user_role":role, "user_id":user.id}

    except Exception as e:
        error_msg = f"Failed to randomly generate {amount} users. Failed at: {user_cnt}/{amount}. Error: {e}"
        logger.error(error_msg)
        return False
    else:
        info_msg = f"Successfully randomly generated {amount} users. Check them out: {users}."
        logger.info(info_msg)
        return users

def randomly_populate_all(amount:int, any_role:bool):
    """
    (* Except for Countries, User_Roles, and Tickets.)
        Returns True upon success, False otherwise.
        "amount" signifies how many users will be created, as long as "any_role" isn't 2.
        If "any_role" is 0, only customer Users and their related Customers table will get populated.
        If "any_role" is 1, all roles and their related tables can get populated at RANDOM.
        If "any_role" is 2, AMOUNT will get OVERWRITTEN to 10, and all roles will get added with tactful proportions: 7/10 customers, 2/10 airlines, 1/10 administrator.
    (* In case all those while loops throw off your internal alarms for potential infinite loops, DW. They're there only as a means for a very unlikely insurance. 
    I skimmed over the data.csv file which 'randominfo' uses, and the other sources that this function bases its data generation upon, and it seems that all the data there is valid 
    by ARS's standards. So this shouldn't be too much of a problem performance-wise. Also, I'll limit the use of this function to 3 times, and only to mode any_role = 2.)
    """
    users = randomly_populate_users(amount=amount, any_role=any_role)
    if not users:
        error_msg = f"The function randomly_populate_users failed at the user stage. Check the other logs for more info."
        logger.error(error_msg)
        return False

    for val in users.values():
        user_id = val['user_id']
        user_role = val['user_role']
        error_msg = ""
        try:
            if user_role == 1: # populate Administrators
                admin_FD = randomly_generate_admin(user_id=user_id)
                while(validate_b4_add(some_model=Administrators, field_data=admin_FD)==False): 
                    admin_FD = randomly_generate_admin(user_id=user_id)
                admin_FD['user_id_id'] = admin_FD.pop('user_id')
                DAL.add_instance(some_model=Administrators, field_data=admin_FD)

            elif user_role == 2: # populate Airline_Companies and Flights
                retries = 0
                airline_FD = randomly_generate_airline(user_id=user_id)
                while(validate_b4_add(some_model=Airline_Companies, field_data=airline_FD)==False):
                    retries += 1
                    # If there would be many airline generations, it will run out of airline names eventually since I had made a list with only a 100 names to choose from, so this is a safety measure for this case.
                    if (retries == 10) : # A stopper. Although there are a 100 names to choose from, I think that a delay of 10 tries signifies that there is already more than enough random data IMO. After all, it's just a tiny project for potential employees with no real world use.
                        error_msg = f"Hey! There's already enough data to fill in the tables IMO. I made sure that trying to populate more data at this point won't be possible, so activating this won't do much from now on."
                        logger.error(error_msg) 
                        raise Exception("In the airline validation part, it failed 10 times in a row.")
                    airline_FD = randomly_generate_airline(user_id=user_id)
                airline_FD['country_id_id'] = airline_FD.pop('country_id')
                airline_FD['user_id_id'] = airline_FD.pop('user_id')
                airline = DAL.add_instance(some_model=Airline_Companies, field_data=airline_FD)
                if (type(airline)==str): # Won't happen, well unless the DB had reached full capacity.
                    error_msg = f"Failed to to add an 'Airline_Companies' instance to the DB within 'randomly_populate_users'. {airline_FD = }"
                    logger.error(error_msg) 
                    raise Exception
                airline = Airline_Companies.objects.get(user_id_id=user_id)

                # Adds 5 flights to each airline
                for i in range(5):
                    flight_FD = randomly_generate_flight(airline_id=airline.id)
                    while(validate_b4_add(some_model=Flights, field_data=flight_FD)==False):
                        flight_FD = randomly_generate_flight(airline_id=airline.id)
                    flight_FD['airline_company_id_id'] = flight_FD.pop('airline_company_id')
                    flight_FD['origin_country_id_id'] = flight_FD.pop('origin_country_id')
                    flight_FD['destination_country_id_id'] = flight_FD.pop('destination_country_id')
                    DAL.add_instance(some_model=Flights, field_data=flight_FD)

            else: # populate Customers
                customer_FD = randomly_generate_customer(user_id=user_id)
                while(validate_b4_add(some_model=Customers, field_data=customer_FD)==False):
                    customer_FD = randomly_generate_customer(user_id=user_id)
                customer_FD['user_id_id'] = customer_FD.pop('user_id')
                DAL.add_instance(some_model=Customers, field_data=customer_FD)

        except Exception as e:
            oh_no = f"Failed to randomly populate all. | {amount = }, {any_role = }, {error_msg = }, {e = } |"
            logger.error(oh_no) 
            return False
    msg = f"Successfully randomly populated all. Go check out the tables! | {amount = }, {any_role = } |"
    logger.info(msg)
    return True

