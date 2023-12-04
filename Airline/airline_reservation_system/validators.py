# Will be used by facade.py before sending add/update requests to dal.py, in order to prevent the input of invalid/illogical data.
# And while at it, prevent the waste of DB server resources on bad requests.

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import re
from airline_reservation_system.models import *
from airline_reservation_system.dal import DAL, get_role_by_user
from PIL import Image
import filetype
import datetime as dt
import pytz
from django.db.models import Q
from phonenumber_field.validators import validate_international_phonenumber
from django.core.files.uploadedfile import SimpleUploadedFile

import logging 
logger = logging.getLogger("pick.me") 


global my_models
my_models = (User_Roles, Users, Customers, Administrators, Airline_Companies , Countries, Flights, Tickets)

def validate_b4_add(some_model:type[models.Model], field_data:dict):
    """
    Don't include id.
    """
    if (some_model not in my_models):
        error_msg = f"Bad input. The given model(={some_model}) is invalid. Valid models: {my_models}."
        logger.error(f"Failed to validate an instance. {error_msg}")
        return False
    if some_model==User_Roles:
        if validate_user_role(role_name=field_data):
            logger.info(f"Successfully validated a user role: {field_data}. You can now use DAL to add it as an instance.")
            return True
    if some_model==Users:
        if validate_user(user_field_data=field_data):
            logger.info(f"Successfully validated a user: {field_data}. You can now use DAL to add it as an instance.")
            return True
    if some_model==Customers:
        if validate_customer(customer_field_data=field_data):
            logger.info(f"Successfully validated a customer: {field_data}. You can now use DAL to add it as an instance.")
            return True
    if some_model==Administrators:
        if validate_administrator(admin_field_data=field_data):
            logger.info(f"Successfully validated an administrator: {field_data}. You can now use DAL to add it as an instance.")
            return True
    if some_model==Airline_Companies:
        if validate_airline_company(airline_field_data=field_data):
            logger.info(f"Successfully validated an airline company: {field_data}. You can now use DAL to add it as an instance.")
            return True
    if some_model==Countries:
        if validate_country(country_field_data=field_data):
            logger.info(f"Successfully validated a country: {field_data}. You can now use DAL to add it as an instance.")
            return True
    if some_model==Flights:
        if validate_flight(flight_field_data=field_data):
            logger.info(f"Successfully validated a flight: {field_data}. You can now use DAL to add it as an instance.")
            return True
    if some_model==Tickets:
        if validate_ticket(ticket_field_data=field_data):
            logger.info(f"Successfully validated a ticket: {field_data}. You can now use DAL to add it as an instance.")
            return True
    return False


def validate_id(some_model:type[models.Model], id:int):
    if type(DAL.get_instance_by_id(some_model=some_model, id=id)) is str:
        return False
    return True


def validate_b4_update(some_model:type[models.Model], field_data:dict, instance:type[models.Model]): #b4_add+id
    """
    RTS: Don't forget to change the keys of the foreign fields so that they'll fit the DAL's field dict format before forwarding the data to it. 
    """
    if (some_model not in my_models):
        error_msg = f"Bad input. The given model is invalid. Valid models: {my_models}."
        logger.error(f"Failed to validate an instance. {error_msg}")
        return False
    
    try:
        if not(isinstance(instance, some_model)):
                error_msg = f"Failed to validate an instance before update. Bad input. 'instance' is not an instance of {some_model}, it is an instance of {type(instance).__name__}."
                logger.error(error_msg)
                return False
    except Exception as e:
        error_msg = (f"Failed to validate an instance before update. Bad input. 'instance' is not an instance of {some_model}.")
        logger.error(f"{error_msg} Error: {e}")
        return False
    
    try:
        id = instance.id
        if not id:
            logger.error("Failed to validate an instance before update. Couldn't get the instance's id.")
            return False 
    except Exception as e:
        error_msg = ("Failed to validate an instance before update. Couldn't get the instance's id.")
        logger.error(f"Failed to validate an instance. {error_msg} Error: {e}")
        return False

    if (some_model not in my_models):
        error_msg = f"Bad input. The given model(={some_model}) is invalid. Valid models: {my_models}."
        logger.error(f"Failed to validate an instance. {error_msg}")
        return False
    if some_model==User_Roles:
        if (validate_user_role(role_name=field_data) and validate_id(some_model=some_model, id=id)):
            logger.info(f"Successfully validated the updated data of a user role (id = {id}). You can now use DAL to update this instance.")
            return True
    if some_model==Users:
        if (validate_user(user_field_data=field_data) and validate_id(some_model=some_model, id=id)):
            logger.info(f"Successfully validated the updated data of a user (id = {id}). You can now use DAL to update this instance.")
            return True
    if some_model==Customers:
        if (validate_customer(customer_field_data=field_data) and validate_id(some_model=some_model, id=id)):
            logger.info(f"Successfully validated the updated data of a customer (id = {id}). You can now use DAL to update this instance.")
            return True
    if some_model==Administrators:
        if (validate_administrator(admin_field_data=field_data) and validate_id(some_model=some_model, id=id)):
            logger.info(f"Successfully validated the updated data of an administrator (id = {id}). You can now use DAL to update this instance.")
            return True
    if some_model==Airline_Companies:
        if (validate_airline_company(airline_field_data=field_data and validate_id(some_model=some_model, id=id))):
            logger.info(f"Successfully validated the updated data of an airline company (id = {id}). You can now use DAL to update this instance.")
            return True
    if some_model==Countries:
        if (validate_country(country_field_data=field_data) and validate_id(some_model=some_model, id=id)):
            logger.info(f"Successfully validated the updated data of a country (id = {id}). You can now use DAL to update this instance.")
            return True
    if some_model==Flights:
        if (validate_flight(flight_field_data=field_data) and validate_id(some_model=some_model, id=id)):
            logger.info(f"Successfully validated the updated data of a flight (id = {id}). You can now use DAL to update this instance.")
            return True
    if some_model==Tickets:
        if (validate_ticket(ticket_field_data=field_data) and validate_id(some_model=some_model, id=id)):
            logger.info(f"Successfully validated the updated data of a ticket (id = {id}). You can now use DAL to update this instance.")
            return True
    return False


def validate_user_role(role_name:str):
    """
    validates a user role.
    returns false if validation fails and vise versa.
    """
    roles = ['Administrator', 'Airline Company', 'Customer']
    if role_name not in roles:
        error_msg = f"Bad input. Failed to validate a user role.'role_name' must be a one of the following: {roles}."
        logger.error(error_msg)
        return False, error_msg
    try:
        role = User_Roles.objects.get(role_name=role_name)
        error_msg = f"User role is valid, but it already exists so it can't be added again. {role_name}'s id is {role.id}."
        logger.error(error_msg)
        return False, error_msg
    except:
        info_msg = f"Successfully validate a user role. 'role_name' = '{role_name}'.)"
        logger.info(info_msg)
        return True, info_msg


def validate_user(user_field_data:dict):
    """
    validates a user.
    returns false if validation fails and vise versa.
    Don't include id and thumbnail.
    Send raw unencrypted password only.
    """

    username = ''
    bad_fields = ['last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'groups', 'user_permissions', 'thumbnail', 'id', 'first_name', 'last_name']
    fields = [field.name for field in Users._meta.get_fields(include_parents=False, include_hidden=False) if (field.name not in bad_fields)]
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

        if key=='user_role':
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
            
    info_msg = f"Successfully validate a user. 'username' = '{username}'.)"
    logger.info(info_msg)
    return True


def validate_customer(customer_field_data:dict):
    """
    validates a customer.
    returns false if validation fails and vise versa.
    Don't include id.
    """
    phone_no = ''
    fields = [field.name for field in Customers._meta.get_fields() if field.name != 'id']
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
            # val = str(val)
            # phone_no = val
            # raw_val = r'{}'.format(val)
            # raw_val = re.sub(r'[^0-9+]', "", raw_val)
            # if not(re.match(r'^\+((?:9[679]|8[035789]|6[789]|5[90]|42|3[578]|2[1-689])|9[0-58]|8[1246]|6[0-6]|5[1-8]|4[013-9]|3[0-469]|2[70]|7|1)(?:\W*\d){0,13}\d$', raw_val)):
            # error_msg = f"Bad input. Failed to validate a customer. '{key}'(={raw_val}) isn't valid."
            # logger.error(error_msg)
            # return False
            # if ( Customers.objects.filter(phone_no=phone_no).exists() ):
            # error_msg = f"Bad input. Failed to validate a customer.'phone_no'(={phone_no}) is already in use by another customer."
            # logger.error(error_msg)
            # return False
        
        if key=='credit_card_no':
            val = str(val)
            raw_val = r'{}'.format(val)
            raw_val = re.sub(r'[^0-9]+', "", raw_val)
            if not(re.match("^(?:4[0-9]{12}(?:[0-9]{3})?|[25][1-7][0-9]{14}|6(?:011|5[0-9][0-9])[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|(?:2131|1800|35\\d{3})\\d{11})$", raw_val)):
                error_msg = f"Bad input. Failed to validate a customer. '{key}'(={raw_val}) isn't valid. Valid credit cards: Visa, MasterCard, American Express, Diners Club, Discover, and JCB."
                logger.error(error_msg)
                return False
            if ( Customers.objects.filter(credit_card_no=val).exists() ):
                error_msg = f"Bad input. Failed to validate a customer.'credit_card_no'(={val}) is already in use by another customer."
                logger.error(error_msg)
                return False
        
        if key=='user_id':
            if not(validate_id(some_model=Users, id=val)):
                error_msg = f"Bad input. Failed to validate a customer. 'user_id' id(={val}) can't be found."
                logger.error(error_msg)
                return False
            role_name = get_role_by_user(user_id=val)
            if (role_name != 'Customer'):
                error_msg = f"Bad input. Failed to validate a customer. The user role of 'user_id' id(={val}) must be 'Customer', not '{role_name}'."
                logger.error(error_msg)
                return False
    
    info_msg = f"Successfully validated a customer. 'phone_no' = '{phone_no}'.)"
    logger.info(info_msg)
    return True


def validate_administrator(admin_field_data:dict):
    """
    validates an administrator.
    returns false if validation fails and vise versa.
    Don't include id.
    """
    user_id = 0
    fields = [field.name for field in Administrators._meta.get_fields() if field.name != 'id']
    keys = list(admin_field_data.keys())
    if (type(admin_field_data) != dict):
        error_msg = f"Bad input. Failed to validate an administrator.'admin_field_data' must be a dictionary."
        logger.error(error_msg)
        return False
    data = admin_field_data
    if sorted(fields)!=sorted(keys):
        error_msg = f"Please make sure that admin_field_data's keys match the field names of {Administrators}. Here are those fields: {fields}, and here are your keys: {keys}."
        logger.error(error_msg)
        return False
    
    for key, val in data.items():

        if (key=='first_name' or key=='last_name'):
            if not((type(val) == str) and (20 >= len(val) >= 2)):
                error_msg = f"Bad input. Failed to validate an administrator.'{key}'(={val}) must be a string with a minimum of 2 characters and a maximum of 20 characters in length."
                logger.error(error_msg)
                return False
            if not(val.isalpha()): 
                error_msg = f"Bad input. Failed to validate an administrator.'{key}'(={val}) can only contain English letters[a-z, A-Z]."
                logger.error(error_msg)
                return False
        
        if key=='user_id':
            user_id = val
            if not(validate_id(some_model=Users, id=val)):
                error_msg = f"Bad input. Failed to validate an administrator. 'user_id' id(={val}) can't be found."
                logger.error(error_msg)
                return False
            role_name = get_role_by_user(user_id=val)
            if (role_name != 'Administrator'):
                error_msg = f"Bad input. Failed to validate an administrator. The user role of 'user_id' id(={val}) must be 'Administrator', not '{role_name}'."
                logger.error(error_msg)
                return False
    
    info_msg = f"Successfully validated an administrator. 'user_id' = '{user_id}'.)"
    logger.info(info_msg)
    return True


def validate_country(country_field_data:dict):
    """
    validates a country.
    returns false if validation fails and vise versa.
    Don't include id.
    """
    name = ''
    fields = [field.name for field in Countries._meta.get_fields() if field.name != 'id']
    keys = list(country_field_data.keys())
    if (type(country_field_data) != dict):
        error_msg = f"Bad input. Failed to validate a country.'country_field_data' must be a dictionary."
        logger.error(error_msg)
        return False
    data = country_field_data
    if sorted(fields)!=sorted(keys):
        error_msg = f"Please make sure that country_field_data's keys match the field names of {Countries}. Here are those fields: {fields}, and here are your keys: {keys}."
        logger.error(error_msg)
        return False
    
    for key, val in data.items():

        if key=='name':
            name = val
            if not((type(val) == str) and (56 >= len(val) >= 2)):
                error_msg = f"Bad input. Failed to validate a country.'{key}'(={val}) must be a string with a minimum of 2 characters and a maximum of 56 characters in length."
                logger.error(error_msg)
                return False
            if not(re.match("^[a-zA-Z- ]*$", val)): 
                error_msg = f"Bad input. Failed to validate a country.'{key}'(={val}) can contain only English letters[a-z, A-Z], '-' and whitespaces."
                logger.error(error_msg)
                return False
            if ( Countries.objects.filter(name=val).exists() ):
                error_msg = f"Bad input. Failed to validate a country.'name'(={name}) already exists in the database."
                logger.error(error_msg)
                return False
        
        if key=='flag':
            try:
                if filetype.is_image(val):
                    continue
            except Exception as e: 
                error_msg = f"Bad input. Failed to validate a country(={name}). 'flag' must be an image. Error: {e}"
                logger.error(error_msg)
                return False
    
    info_msg = f"Successfully validated a country. 'name' = '{name}'.)"
    logger.info(info_msg)
    return True

def validate_airline_company(airline_field_data:dict):
    """
    validates an airline company.
    returns false if validation fails and vise versa.
    Don't include id.
    """
    user_id = 0
    fields = [field.name for field in Airline_Companies._meta.get_fields() if field.name != 'id']
    keys = list(airline_field_data.keys())
    if (type(airline_field_data) != dict):
        error_msg = f"Bad input. Failed to validate an airline company.'airline_field_data' must be a dictionary."
        logger.error(error_msg)
        return False
    data = airline_field_data
    if sorted(fields)!=sorted(keys):
        error_msg = f"Please make sure that airline_field_data's keys match the field names of {Airline_Companies}. Here are those fields: {fields}, and here are your keys: {keys}."
        logger.error(error_msg)
        return False
    
    for key, val in data.items():

        if key=='name':
            name = val
            if not((type(val) == str) and (30 >= len(val) >= 2)):
                error_msg = f"Bad input. Failed to validate an airline company. '{key}'(={val}) must be a string with a minimum of 2 characters and a maximum of 30 characters in length."
                logger.error(error_msg)
                return False
            if not(re.match("^[a-zA-Z- ]*$", val)): 
                error_msg = f"Bad input. Failed to validate an airline company. '{key}'(={val}) can contain only English letters[a-z, A-Z], '-' and whitespaces."
                logger.error(error_msg)
                return False
            if ( Airline_Companies.objects.filter(name=val).exists() ):
                error_msg = f"Bad input. Failed to validate an airline company. 'name'(={val}) already exists in the database."
                logger.error(error_msg)
                return False
            
        if key=='country_id':
            if not(validate_id(some_model=Countries, id=val)):
                error_msg = f"Bad input. Failed to validate an airline company. 'country_id' id(={val}) can't be found."
                logger.error(error_msg)
                return False
        
        if key=='user_id':
            user_id = val
            if not(validate_id(some_model=Users, id=val)):
                error_msg = f"Bad input. Failed to validate an airline company. 'user_id' id(={val}) can't be found."
                logger.error(error_msg)
                return False
            role_name = get_role_by_user(user_id=val)
            if (role_name != 'Airline Company'):
                error_msg = f"Bad input. Failed to validate an airline company. The user role of 'user_id' id(={val}) must be 'Airline Company', not '{role_name}'."
                logger.error(error_msg)
                return False
        
    info_msg = f"Successfully validated an airline company, 'name' = '{name}'. 'user_id' = '{user_id}'.)"
    logger.info(info_msg)
    return True

def validate_flight(flight_field_data:dict):
    """
    validates a flight company.
    returns false if validation fails and vise versa.
    Don't include id.
    """
    origin = 0
    departure_time = ''
    fields = [field.name for field in Flights._meta.get_fields() if field.name != 'id']
    keys = list(flight_field_data.keys())
    if (type(flight_field_data) != dict):
        error_msg = f"Bad input. Failed to validate a flight company.'flight_field_data' must be a dictionary."
        logger.error(error_msg)
        return False
    data = flight_field_data
    if sorted(fields)!=sorted(keys):
        error_msg = f"Please make sure that flight_field_data's keys match the field names of {Administrators}. Here are those fields: {fields}, and here are your keys: {keys}."
        logger.error(error_msg)
        return False
    
    for key, val in data.items():

        if key=='airline_company_id':
            airline = val
            if not(validate_id(some_model=Airline_Companies, id=val)):
                error_msg = f"Bad input. Failed to validate a flight. 'airline_company_id' id(={val}) can't be found."
                logger.error(error_msg)
                return False
            
        if key=='origin_country_id':
            origin = val
            if not(validate_id(some_model=Countries, id=val)):
                error_msg = f"Bad input. Failed to validate a flight. 'origin_country_id' id(={val}) can't be found."
                logger.error(error_msg)
                return False
        
        if key=='destination_country_id':
            if (not(validate_id(some_model=Countries, id=val))):
                error_msg = f"Bad input. Failed to validate a flight. 'destination_country_id' id(={val}) can't be found."
                logger.error(error_msg)
                return False
            if origin == val:
                error_msg = f"Bad input. Failed to validate a flight. 'destination_country_id' id(={val}) can't be the same as origin_country_id."
                logger.error(error_msg)
                return False
        
        if key=='departure_time':
            departure_time = val
            if not(isinstance(val, dt.datetime)):
                error_msg = f"Bad input. Failed to validate a flight. 'departure_time'(={val}) is not a datetime object."
                logger.error(error_msg)
                return False
            val_str = val.strftime('%Y-%m-%d')
            if not(dt.date.fromisoformat(val_str)):
                error_msg = f"Bad input. Failed to validate a flight. 'departure_time'(={val}) is in an incorrect data format, the format should be 'YYYY-MM-DD'."
                logger.error(error_msg)
                return False
            # print(val, 'type: ', type(val))
            start = dt.datetime(year=1909, month=11, day=16)
            too_far = val + dt.timedelta(days=365)
            # print(f'1-thisssssssss: ({dt.datetime.now()} <= {val} <= {too_far}) ', ' = ',(dt.datetime.now() <= val <= too_far) )# decided to let users input old flights too (flights which includes times before now), so this isn't relevant anymore. But I'll leave this here in case I change my mind later.
            if ((val < start) or ( val >= too_far) ): # On November 16, 1909, the world's first airline, DELAG (Deutsche Luftschiffahrts-Aktiengesellschaft or German Airship Company) was established.
                error_msg = f"Bad input. Failed to validate a flight. 'departure_time'(={val}) should be after 1909/11/16 and before a year from now which is {too_far}."
                logger.error(error_msg)
                return False
        
        if key=='landing_time':
            landing_time = val
            if not(isinstance(val, dt.datetime)):
                error_msg = f"Bad input. Failed to validate a flight. 'landing_time'(={val}) is not a datetime object."
                logger.error(error_msg)
                return False
            val_str = val.strftime('%Y-%m-%d')
            if not(dt.date.fromisoformat(val_str)):
                error_msg = f"Bad input. Failed to validate a flight. 'landing_time'(={val}) is in an incorrect data format, the format should be 'YYYY-MM-DD'."
                logger.error(error_msg)
                return False
            too_far = departure_time + dt.timedelta(hours=20)
            too_short = departure_time + dt.timedelta(minutes=30)
            print(f'2-thisssssssss: ({too_short} <= {val} <= {too_far}) ', ' = ',(too_short <= val <= too_far) )
            if ((val < start) or not(too_short <= val <= too_far) ): 
                error_msg = f"Bad input. Failed to validate a flight. 'landing_time'(={val}), is invalid because the duration of a flight can not be shorter than half an hour, or longer than 20 hours. So the landing time should be after {too_short} and before {too_far}."
                logger.error(error_msg)
                return False
        
        if key=='remaining_tickets':
            if not(type(val) is int):
                error_msg = f"Bad input. Failed to validate a flight. 'remaining_tickets'(={val}) must be an integer."
                logger.error(error_msg)
                return False
            if not(0 <= val <= 860):
                error_msg = f"Bad input. Failed to validate a flight. 'remaining_tickets'(={val}) can not be a negative number, or bigger than 860."
                logger.error(error_msg)
                return False
    
    info_msg = f"Successfully validated a flight. 'airline_company_id' = '{airline}', 'departure_time' = '{departure_time}', 'landing_time' = '{landing_time}'.)"
    logger.info(info_msg)
    return True

def validate_ticket(ticket_field_data:dict):
    """
    validates a ticket.
    returns false if validation fails and vise versa.
    Don't include id.
    """
    flight_id = 0
    customer_id = 0
    fields = [field.name for field in Tickets._meta.get_fields() if field.name != 'id']
    keys = list(ticket_field_data.keys())
    if (type(ticket_field_data) != dict):
        error_msg = f"Bad input. Failed to validate a ticket.'ticket_field_data' must be a dictionary."
        logger.error(error_msg)
        return False
    data = ticket_field_data
    if sorted(fields)!=sorted(keys):
        error_msg = f"Please make sure that ticket_field_data's keys match the field names of {Tickets}. Here are those fields: {fields}, and here are your keys: {keys}."
        logger.error(error_msg)
        return False
    # print(data.items())
    for key, val in data.items():
    
        if key=='flight_id':
            flight_id = val
            if not(validate_id(some_model=Flights, id=val)):
                error_msg = f"Bad input. Failed to validate a ticket. 'flight_id' id(={val}) can't be found."
                logger.error(error_msg)
                return False
            
        if key=='customer_id':
            customer_id = val
            if not(validate_id(some_model=Customers, id=val)):
                error_msg = f"Bad input. Failed to validate a ticket. 'customer_id' id(={val}) can't be found."
                logger.error(error_msg)
                return False
        
        try:
            if (Tickets.objects.filter(Q(flight_id=flight_id), Q(customer_id=customer_id)).exists() ):
                error_msg = f"Bad input. Failed to validate a ticket. A ticket with the given data: 'customer_id' = {customer_id}, 'flight_id' = {flight_id}, already exists in the database."
                logger.error(error_msg)
                return False
            continue
        except Exception as e:
            logger.error(f"Bad input. Failed to validate a ticket. Ticket database search failed. error: {e}")
            return False

    info_msg = f"Successfully validated a ticket. 'customer_id' = {customer_id}, 'flight_id' = {flight_id}.)"
    logger.info(info_msg)
    return True

def validate_instance_type(some_model:type[models.Model], instance:models.Model):
    try:
        if not(isinstance(instance, some_model)):
            error_msg = f"Failed to validate an instance before update. Bad input. 'instance' is not an instance of {some_model}."
            logger.error(error_msg)
            return False
    except Exception as e:
        error_msg = (f"Failed to validate an instance before update. Bad input. 'instance' is not an instance of {some_model}.")
        logger.error(f"{error_msg} Error: {e}")
        return False

