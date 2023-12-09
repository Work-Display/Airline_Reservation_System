from .models import *
from django.db import models
from django.db.models import Q
import datetime as dt
from datetime import datetime, timedelta
from django.core.files.uploadedfile import SimpleUploadedFile
import os.path

import logging 
logger = logging.getLogger("pick.me") 


from django.apps import apps

class DAL:
    """
    Provides generalized CRUD services to each one of my models. 
    Which include: 'get_instance_by_id', 'get_all_instances', 'add_instance', 'add_all_instances', 'update_instance', 'remove_instance'.
    [On a side note, in the project's assignment document they asked for this to be a class, but I don't see a reason for this to be a class.
    And that's because it would never have object instances, and nor will I ever need to inherit from it. Perhaps I am missing something?]
    """
    global my_models
    my_models = (User_Roles, Users, Customers, Administrators, Airline_Companies , Countries, Flights, Tickets)

    # RTS(-reminder to self, ignore those if you're not me): "static method can be called on the class itself, rather than on an instance of the class."
    @staticmethod
    def get_id_from_instance(instance:models.Model):
        try:
            id = instance.id
            if not id:
                logger.error("Failed to get the instance's id.")
                return False 
        except Exception as e:
            logger.error(f"Failed to get the instance's id. Error: {e}")
            return False
        return id

    @staticmethod
    def get_instance_by_id(some_model:type[models.Model], id:int):
        if ((type(id) is int) and (id>0)):
            if (some_model in my_models):
                try:
                    instance = some_model.objects.get(id=id)
                    logger.info(f"Successfully got the {some_model} instance, pk={id}.")
                    return instance
                except Exception:
                    error_msg = f"No {some_model} with this id was found."
                    logger.error(f"Failed to get the instance. {error_msg}")
                    return error_msg
            else:
                error_msg = f"Bad input. The given model is invalid. Valid models: {my_models}."
                logger.error(f"Failed to get the instance. {error_msg}")
                return error_msg
        else:
            error_msg = "Bad input. Id must be a positive integer."
            logger.error(f"Failed to get the instance. {error_msg}")
            return error_msg
        
    @staticmethod
    def get_all_instances(some_model:type[models.Model]):
        if (some_model in my_models):
            try:
                instances = some_model.objects.all()
                logger.info(f"Successfully got all instances.")
                return instances
            except Exception:
                error_msg = f"{some_model} has no instances."
                logger.error(f"Failed to get all instances. {error_msg}")
                return error_msg
        else:
            error_msg = f"Bad input. The given model is invalid. Valid models: {my_models}."
            logger.error(f"Failed to get all instances. {error_msg}")
            return error_msg

    @staticmethod
    def add_instance(some_model:type[models.Model], field_data:dict):
        if (some_model in my_models):
            try:
                fields = [field.name for field in some_model._meta.get_fields(include_parents=False, include_hidden=False) if field.name!='id'] #RTS: you changed 'reverse' to 'False'
                # keys = list(field_data.keys())
                new_instance = some_model() 
                for key, value in field_data.items():
                    if hasattr(new_instance, key):

                        print(type(key), '=', key)
                        print(f"{key} = {value}")

                        # special cases
                        if (key=='password'):
                            new_instance.set_password(field_data[key])
                        elif ((key=='user_role_id') and (value==1)):
                            setattr(new_instance, key, value)
                            setattr(new_instance, 'is_superuser', value)
                            setattr(new_instance, 'is_staff', value)
                        else: # default 
                            setattr(new_instance, key, value)

                new_instance.save()
                logger.info(f"Successfully added {some_model} instance, pk={new_instance.pk}.")
                return new_instance
            except Exception as e:
                error_msg = f"Please make sure that field_data's keys match the field names of {some_model}. Here are those fields: {fields}."
                logger.error(f"Failed to add an instance. {error_msg} e:{e}.")
                return error_msg
        else:
            error_msg = f"Bad input. The given model is invalid. Valid models: {my_models}."
            logger.error(f"Failed to add an instance. {error_msg}")
            return error_msg
    
    @staticmethod
    def add_all_instances(some_model:type[models.Model], new_instances:list[type[models.Model]]):
        """
        You must validate each individual instance in 'new_instances' before sending them here!
        """
        if (some_model in my_models):
            try:
                for instance in new_instances:
                    if (not (instance.isinstance(some_model))):
                        raise Exception
                    instance.save()
                # RTS, bad practice: logger.info(f"Successfully added all instances: first={new_instances[0]} - last={new_instances[-1]}.")
                logger.info(f"Successfully added all instances.")
                return new_instances
            except Exception:
                error_msg = f"Please make sure that every instance in new_instances is an instance of the model {some_model}."
                logger.error(f"Failed to add all instances. {error_msg}")
                return error_msg
        else:
            error_msg = f"Bad input. The given model is invalid. Valid models: {my_models}."
            logger.error(f"Failed to add all instances. {error_msg}")
            return error_msg
        
    @staticmethod
    def update_instance(some_model:type[models.Model], instance:type[models.Model], field_data:dict):
        if ( (some_model in my_models) and ((DAL.get_instance_by_id(some_model=some_model, id=id)) is not str) ):
            try:
                fields = [field.name for field in some_model._meta.get_fields()]
                for key, value in field_data.items():
                    if hasattr(instance, key):
                        if (key=='password'):
                            instance.set_password(field_data[key])
                        else:
                            setattr(instance, key, value)
                instance.save()
                logger.info(f"Successfully updated an instance.")
                return instance
            except Exception:
                error_msg = f"Please make sure that field_data's keys match the field names of {some_model}. Here are those fields: {fields}."
                logger.error(f"Failed to update an instance. {error_msg}")
                return error_msg
        else:
            error_msg = f"Bad input. The given model is invalid OR/AND the provided instance isn't an instance of {some_model}. Valid models: {my_models}. The provided instance belongs to the model: {type(instance)}."
            logger.error(f"Failed to update an instance. {error_msg}")
            return error_msg
        
    @staticmethod
    def remove_instance(some_model:type[models.Model], instance:models.Model):
        
        id = DAL.get_id_from_instance(instance=instance)

        if id==False:
            error_msg = f"Failed to remove an instance. Bad input. Couldn't get the id of 'instance'."
            logger.error(error_msg)
            return False, error_msg

        if ( (some_model in my_models) and ((DAL.get_instance_by_id(some_model=some_model, id=id)) is not str) ):
            instance.delete()
            msg = f"Successfully removed an instance from {some_model}, the id of the removed instance was: id = {id}."
            logger.info(msg)
            return True, msg
        else:
            error_msg = f"Failed to remove an instance. Bad input. The given model is invalid OR/AND the provided instance isn't an existing instance of {some_model}. Valid models: {my_models}. The provided instance belongs to the model: {type(instance)}."
            logger.error(error_msg)
            msg = f"Failed to remove an instance from {some_model}, id = {id}."
            return False, msg

    @staticmethod
    def get_instances_by_name(some_model:type[models.Model], name:str):
        """
        Searches within "some_model" for the instances that contain "name" in their name field.
        It then returns these instances if it succeeded, and returns False upon failure. 
        """
        named_models = {Users:1, Customers:2, Administrators:2, Airline_Companies:3 , Countries:3} # name_fields = {1:"username", 2:"first_name", 3:"name"}
        if type(name) is str:
            if (some_model in named_models.keys()):
                name_key = named_models[some_model]
                try:
                    if name_key==1:
                        instances = some_model.objects.filter(username__icontains=name)
                    elif name_key==2:
                        instances = some_model.objects.filter( Q(first_name__icontains=name) | Q(last_name__icontains=name))
                    else:
                        instances = some_model.objects.filter(name__icontains=name)
                    logger.info(f"Successfully found the instances of {some_model} which contained {name = }, instances={instances}.")
                    if instances:
                        return instances
                    info_msg = f"{some_model} doesn't have any instances which contain {name = }."
                    logger.info(info_msg)
                    return False
                except Exception as e:
                    error_msg = f"{some_model} doesn't have any instances which contain {name = }."
                    logger.error(f"Failed to get instances of {some_model} by {name = }. {error_msg} {e}")
                    return False
            else:
                error_msg = f"Bad input. The given model = {some_model}, is invalid. Valid models: {named_models}."
                logger.error(f"Failed to get instances of {some_model} by {name = }. {error_msg}")
                return False
        else:
            error_msg = "Bad input. Name must be a string."
            logger.error(f"Failed to get the instances of {some_model} by {name = }. {error_msg}")
            return False
        
    @staticmethod
    def get_id_by_name(some_model:type[models.Model], name:str):
        """
        Created for the advanced flight search.
        'some_model' can be either Countries or Airline_Companies.
        Upon success it returns the id of the {some_model} instance whose name = {name}.
        Upon failure it returns None. 
        """
        valid_models = (Airline_Companies, Countries)
        if type(name) is str:
            if (some_model in valid_models):
                try:
                    instances = DAL.get_instances_by_name(some_model=some_model, name=name)
                    if (type(instances) is False):
                        logger.info(f"{some_model} doesn't have any instances with {name = }.")
                        return None
                    if instances.count() == 1:
                        obj = instances.first()
                        id = obj.id
                        logger.info(f"{some_model} has an instance with {name = }, and its {id = }.")
                        return id
                    else:
                        logger.info(f"{some_model} doesn't have any instances with {name = } (the country name search came up with more than 1 result).")
                        return None
                except Exception as e:
                    logger.error(f"Failed to get the id of the {some_model} instance with {name = }. Error: {e}")
                    return None
            else:
                error_msg = f"Bad input. The given model = {some_model}, is invalid. Valid models: {valid_models}."
                logger.error(f"Failed to get the id of the {some_model} instance with {name = }. {error_msg}")
                return None
        else:
            error_msg = f"Bad input. 'name' = {name} must be a string."
            logger.error(f"Failed to get the id of the {some_model} instance with {name = }. {error_msg}")
            return None
        
    @staticmethod
    def get_name_by_id(some_model:type[models.Model], id:int):
        """
        'some_model' can be either Countries or Airline_Companies.
        Upon success it returns the name of the {some_model} instance whose id = {id}.
        Upon failure it returns False. 
        """
        valid_models = (Airline_Companies, Countries)
        if type(id) is int:
            if (some_model in valid_models):
                try:
                    instance = DAL.get_instance_by_id(some_model=some_model, id=id)
                    if (type(instance) is str):
                        raise Exception(f"{some_model} doesn't have any instances with {id = }.")
                    name = instance.name
                    logger.info(f"Successfully got the {name = }, of the {some_model} instance with {id = }.")
                    return name
                except Exception as e:
                    logger.error(f"Failed to get the name of the {some_model} instance with {id = }. Error: {e}")
                    return False
            else:
                error_msg = f"Bad input. The given model = {some_model}, is invalid. Valid models: {valid_models}."
                logger.error(f"Failed to get the name of the {some_model} instance with {id = }. {error_msg}")
                return False
        else:
            error_msg = f"Bad input. 'id' = {id} must be an integer."
            logger.error(f"Failed to get the name of the {some_model} instance with {id = }. {error_msg}")
            return False

# ===========================================================================================================================
# USER:


def get_user_by_username(username:str):
    try: 
        r = Users.objects.get(username=username)
        logger.info("Success.")
        return r
    except Exception as e:
        logger.error(f"Failure. {e}")
        return e


# ===========================================================================================================================
# CUSTOMER:


def get_customer_by_username(username:str):
    try: 
        r = Customers.objects.get(users__username=username)
        logger.info("Success.")
        return r
    except Exception as e:
        logger.error(f"Failure. {e}")
        return e


# ===========================================================================================================================
# AIRLINES:


def get_airlines_by_countryID(country_id:int):
    country = DAL.get_instance_by_id(Countries, country_id)
    try: 
        r = country.airlines
        logger.info("Success.")
        return r
    except Exception as e:
        logger.error(f"Failure. {e}")
        return e
    
def get_airline_by_username(username:str):
    try: 
        r = Airline_Companies.objects.get(users__username=username)
        logger.info("Success.")
        return r
    except Exception as e:
        logger.error(f"Failure. {e}")
        return e    
    
def get_airlines_by_parameters_S(name:str, country_id:int, user_id:int):
    try:
        airlines = Airline_Companies.objects.filter(Q(name=name),
                                                    Q(country_id=country_id),
                                                    Q(user_id=user_id))
        logger.info("Success.")
        return airlines
    except Exception as e:
        err_msg = f"Failed to get airline companies by parameters. {e}"
        logger.error(err_msg)
        return err_msg

def get_airlines_by_parameters_D(filters:dict):

    if (type(filters)!=dict):
        err_msg = f"Bad input. Failed to get airline companies by parameters, 'filters' must be a dictionary, not {type(filters)}."
        logger.error(err_msg)
        return err_msg
    
    if (len(filters)<1):
        err_msg = f"Bad input. Failed to get airline companies by parameters, 'filters' must be a dictionary with at least one item."
        logger.error(err_msg)
        return err_msg
    
    valid_filters = ['name', 'country_id_id']
    logger.info(f"received this: {filters = }")
    good_filters = {
    key: value
    for key, value in filters.items()
    if ((key in valid_filters) and (value!=None))
    }

    if (len(good_filters)<1):
        err_msg = f"Bad input. Failed to get airline companies by parameters, 'filters' must be a dictionary with at least one valid filter name key. {valid_filters = }."
        logger.error(err_msg)
        return err_msg
    
    try:
        airlines = Airline_Companies.objects.filter(**good_filters)
        logger.info("Successfully got airline companies by parameters.")
        return airlines
    except Exception as e:
        err_msg = f"Failed to get airline companies by parameters, {filters = }. Error: {e}"
        logger.error(err_msg)
        return err_msg

# ===========================================================================================================================
# FLIGHTS:


def get_flights_by_origin_countyID(country_id:int):
    country = DAL.get_instance_by_id(Countries, country_id)
    try: 
        r = country.flight_origin
        logger.info("Success.")
        return r
    except Exception as e:
        logger.error(f"Failure. {e}")
        return e

def get_flights_by_destination_countyID(country_id:int):
    country = DAL.get_instance_by_id(Countries, country_id)
    try: 
        r = country.flight_destination
        logger.info("Success.")
        return r
    except Exception as e:
        logger.error(f"Failure. {e}")
        return e

def get_flights_by_departure_date(date:datetime.date):
    try: 
        r = Flights.objects.filter(departure_time__date=date)
        logger.info("Success.")
        return r
    except Exception as e:
        logger.error(f"Failure. {e}")
        return e

def get_flights_by_landing_date(date:datetime.date):
    try: 
        r = Flights.objects.filter(landing_time__date=date)
        logger.info("Success.")
        return r
    except Exception as e:
        logger.error(f"Failure. {e}")
        return e

def get_flights_by_customerID(customer_id:int):
    try: 
        tickets = Tickets.objects.filter(customer_id=customer_id)
        flights = []
        for ticket in tickets:
            flights.append(ticket.flight)
        logger.info("Success.")
        return flights
    except Exception as e:
        logger.error(f"Failure. {e}")
        return e

def get_flights_by_parameters_S(origin_country_id:int, destination_country_id:int, date:datetime.date):
    # RTS, inefficient practice:
    # flights = Flights.objects.filter(origin_country_id=origin_country_id)
    # flights = flights.filter(destination_country_id=destination_country_id)
    # flights = flights.filter(departure_time__date=date)
    try:
        flights = Flights.objects.filter(Q(origin_country_id=origin_country_id),
                                         Q(destination_country_id=destination_country_id),
                                         Q(departure_time__date=date))
        logger.info("Succeeded to get flights by parameters.")
        return flights
    except Exception as e:
        err_msg = f"Failed to get flights by parameters. {e}"
        logger.error(err_msg)
        return err_msg

def get_flights_by_parameters_D(filters:dict):

    # logger.info(f"received this: {filters = }")
    if (type(filters)!=dict):
        err_msg = f"Bad input. Failed to get flights by parameters, 'filters' must be a dictionary, not {type(filters)}."
        logger.error(err_msg)
        return err_msg
    
    if (len(filters)<1):
        err_msg = f"Bad input. Failed to get flights by parameters, 'filters' must be a dictionary with at least one item."
        logger.error(err_msg)
        return err_msg
    
    valid_filters = ['airline_company_id_id', 'origin_country_id_id', 'destination_country_id_id', 'departure_time', 'landing_time', 'remaining_tickets']
    good_filters = {
    key: value
    for key, value in filters.items()
    if ((key in valid_filters) and (value!=None))
    }

    if (len(good_filters)<1):
        err_msg = f"Bad input. Failed to get flights by parameters, 'filters' must be a dictionary with at least one valid filter name key. {valid_filters = }."
        logger.error(err_msg)
        return err_msg
    
    # logger.info(f"turned it to this: {good_filters = }")
    try:
        flights = Flights.objects.filter(**good_filters)
        logger.info("Successfully got flights by parameters.")
        # logger.info(f"returned this: {flights = }")
        return flights
    except Exception as e:
        err_msg = f"Failed to get flights by parameters, {filters = }. Error: {e}"
        logger.error(err_msg)
        return err_msg


def get_flights_by_parameters_DA(filters:dict):
    """
    DA stands for dynamic & advanced.
    It works with some name field inputs instead of with ids, and that's what differs it from other versions of this filtering functionality.
    This one is currently being used used on the flights page, while the other 'get_flights_by_parameters' functions are just collecting dust. 
    """

    if (type(filters)!=dict):
        err_msg = f"Bad input. Failed to get flights by parameters, 'filters' must be a dictionary, not {type(filters)}."
        logger.error(err_msg)
        return err_msg
    
    if (len(filters)<1):
        err_msg = f"Bad input. Failed to get flights by parameters, 'filters' must be a dictionary with at least one item."
        logger.error(err_msg)
        return err_msg
    
    valid_filters = ['airline_company', 'origin_country', 'destination_country', 'departure_time', 'landing_time', 'remaining_tickets']
    good_filters = {
    key: value
    for key, value in filters.items()
    if ((key in valid_filters) and (value!=None))
    }

    if (len(good_filters)<1):
        err_msg = f"Bad input. Failed to get flights by parameters, 'filters' must be a dictionary with at least one valid filter name key. {valid_filters = }."
        logger.error(err_msg)
        return err_msg
    
    edited_filters = {}
    for key, val in good_filters.items():
        if key == 'airline_company':
            id = DAL.get_id_by_name(some_model=Airline_Companies, name=val)
            if id != None:
                edited_filters['airline_company_id_id'] = id
        elif key == 'origin_country' or key == 'destination_country':
            id = DAL.get_id_by_name(some_model=Countries, name=val)
            if id != None:
                edited_filters[key + '_id_id'] = id
        else:
            edited_filters[key] = val

    try:
        flights = Flights.objects.filter(**edited_filters)
        logger.info("Successfully got flights by parameters.")
        return flights
    except Exception as e:
        err_msg = f"Failed to get flights by parameters, {filters = }. Error: {e}"
        logger.error(err_msg)
        return err_msg



def get_flights_by_airlineID(airline_id:int):
    try: 
        flights = Flights.objects.filter(airline_company_id=airline_id)
        logger.info(f"Succeeded to get flights by airline_company_id = {airline_id}.")
        return flights
    except Exception as e:
        err_msg = f"Failed to get flights by airline_company_id = {airline_id}. Error: {e}"
        logger.error(err_msg)
        return err_msg


def get_arriving_flights(country_id:int):
    """
    returns all the flights which will arrive at the given country within 12 hours from now.
    """
    try:
        country = Countries.objects.get(id=country_id)
        if country:
            flights = Flights.objects.filter(Q(destination_country_id=country_id),
                                             Q(landing_time__gte=datetime.now()),
                                             Q(landing_time__lte=(datetime.now() + timedelta(hours=12))))
            logger.info("Success.")
            return flights
        err_msg = f"Failure. Country with id={country_id} wasn't found."
        logger.error(err_msg)
        return err_msg
    except Exception as e:
        logger.error(f"Failure. {e}")
        return e

def get_departing_flights(country_id:int):
    """
    returns all the flights which will depart from the given country within 12 hours from now.
    """
    try:
        country = Countries.objects.get(id=country_id)
        if not country: # RTS: This approach is more readable in comparison to the one above.
            err_msg = f"Failure. Country with id={country_id} wasn't found."
            logger.error(err_msg)
            return err_msg
        flights = Flights.objects.filter(Q(origin_country_id=country_id),
                                         Q(departure_time__gte=datetime.now()),
                                         Q(departure_time__lte=(datetime.now() + timedelta(hours=12))))
        logger.info("Success.")
        return flights
    except Exception as e:
        logger.error(f"Failure. {e}")
        return e


# ===========================================================================================================================
# TICKETS:


def get_tickets_by_customer(customer_id:int):
    try: 
        customer_id = int(customer_id)
        tickets = Tickets.objects.filter(customer_id_id=customer_id).all()
        logger.info(f"Succeeded to get tickets by customer_id = {customer_id}.")
        return tickets
    except Exception as e:
        err_msg = f"Failed to get tickets by customer_id = {customer_id}. {e}"
        logger.error(err_msg)
        return err_msg


# ===========================================================================================================================
# USER ROLES:


def populate_user_roles():
    roles = ['Administrator', 'Airline Company', 'Customer']
    cnt = 0
    try: 
        for role in roles:
            role_FD = {'role_name':role}
            r = DAL.add_instance(some_model=User_Roles, field_data=role_FD)
            if type(r) is str:
                raise Exception("Failed to add a user role instance within 'populate_user_roles'.")
            cnt += 1 
        logger.info(f"Successfully added {cnt} user roles.")
        return True
    except Exception as e:
        logger.error(f"Failed to populate user roles. Failed at {cnt}/{len(roles)}. error: {e}")
        return False

def get_role_by_user(user_id:str):
    """
    returns a user role name string.
    returns false if user id does not exists and if 'role_name' can't be returned.
    """
    if (type(user_id) != int):
        error_msg = f"Bad input. 'get_role_by_user' failed. 'user_id'(={user_id}) must be an int."
        logger.error(error_msg)
        return False
    roles = ['Administrator', 'Airline Company', 'Customer']
    user = DAL.get_instance_by_id(id=user_id, some_model=Users)
    if type(user) is str:
        error_msg = f"Bad input. 'get_role_by_user' failed. A user with this id: {user_id} does not exists."
        logger.error(error_msg)
        return False
    role_id = user.user_role_id
    role = User_Roles.objects.get(id=role_id)
    if not role:
        error_msg = f"Bad input. 'get_role_by_user' failed. A user role with this id: {role_id} does not exists."
        logger.error(error_msg)
        return False
    role_name = role.role_name
    if (role_name and role_name not in roles):
        error_msg = f"Bad data found. 'get_role_by_user' failed. 'role_name' isn't valid."
        logger.error(error_msg)
        return False
    else:
        info_msg = f"'role_name'(={role_name}) was successfully found and returned."
        logger.info(info_msg)
        return role_name
 

# ===========================================================================================================================
# COUNTRIES:


def populate_countries():
    country_to_abbrev = {
        "Andorra": "AD",
        "United Arab Emirates": "AE",
        "Afghanistan": "AF",
        "Antigua and Barbuda": "AG",
        "Anguilla": "AI",
        "Albania": "AL",
        "Armenia": "AM",
        "Angola": "AO",
        "Antarctica": "AQ",
        "Argentina": "AR",
        "American Samoa": "AS",
        "Austria": "AT",
        "Australia": "AU",
        "Aruba": "AW",
        "Åland Islands": "AX",
        "Azerbaijan": "AZ",
        "Bosnia and Herzegovina": "BA",
        "Barbados": "BB",
        "Bangladesh": "BD",
        "Belgium": "BE",
        "Burkina Faso": "BF",
        "Bulgaria": "BG",
        "Bahrain": "BH",
        "Burundi": "BI",
        "Benin": "BJ",
        "Saint Barthélemy": "BL",
        "Bermuda": "BM",
        "Brunei Darussalam": "BN",
        "Bolivia (Plurinational State of)": "BO",
        "Bonaire, Sint Eustatius and Saba": "BQ",
        "Brazil": "BR",
        "Bahamas": "BS",
        "Bhutan": "BT",
        "Bouvet Island": "BV",
        "Botswana": "BW",
        "Belarus": "BY",
        "Belize": "BZ",
        "Canada": "CA",
        "Cocos (Keeling) Islands": "CC",
        "Congo, Democratic Republic of the": "CD",
        "Central African Republic": "CF",
        "Congo": "CG",
        "Switzerland": "CH",
        "Côte d'Ivoire": "CI",
        "Cook Islands": "CK",
        "Chile": "CL",
        "Cameroon": "CM",
        "China": "CN",
        "Colombia": "CO",
        "Costa Rica": "CR",
        "Cuba": "CU",
        "Cabo Verde": "CV",
        "Curaçao": "CW",
        "Christmas Island": "CX",
        "Cyprus": "CY",
        "Czechia": "CZ",
        "Germany": "DE",
        "Djibouti": "DJ",
        "Denmark": "DK",
        "Dominica": "DM",
        "Dominican Republic": "DO",
        "Algeria": "DZ",
        "Ecuador": "EC",
        "Estonia": "EE",
        "Egypt": "EG",
        "Western Sahara": "EH",
        "Eritrea": "ER",
        "Spain": "ES",
        "Ethiopia": "ET",
        "Finland": "FI",
        "Fiji": "FJ",
        "Falkland Islands (Malvinas)": "FK",
        "Micronesia (Federated States of)": "FM",
        "Faroe Islands": "FO",
        "France": "FR",
        "Gabon": "GA",
        "United Kingdom of Great Britain and Northern Ireland": "GB",
        "Grenada": "GD",
        "Georgia": "GE",
        "French Guiana": "GF",
        "Guernsey": "GG",
        "Ghana": "GH",
        "Gibraltar": "GI",
        "Greenland": "GL",
        "Gambia": "GM",
        "Guinea": "GN",
        "Guadeloupe": "GP",
        "Equatorial Guinea": "GQ",
        "Greece": "GR",
        "South Georgia and the South Sandwich Islands": "GS",
        "Guatemala": "GT",
        "Guam": "GU",
        "Guinea-Bissau": "GW",
        "Guyana": "GY",
        "Hong Kong": "HK",
        "Heard Island and McDonald Islands": "HM",
        "Honduras": "HN",
        "Croatia": "HR",
        "Haiti": "HT",
        "Hungary": "HU",
        "Indonesia": "ID",
        "Ireland": "IE",
        "Israel": "IL",
        "Isle of Man": "IM",
        "India": "IN",
        "British Indian Ocean Territory": "IO",
        "Iraq": "IQ",
        "Iran (Islamic Republic of)": "IR",
        "Iceland": "IS",
        "Italy": "IT",
        "Jersey": "JE",
        "Jamaica": "JM",
        "Jordan": "JO",
        "Japan": "JP",
        "Kenya": "KE",
        "Kyrgyzstan": "KG",
        "Cambodia": "KH",
        "Kiribati": "KI",
        "Comoros": "KM",
        "Saint Kitts and Nevis": "KN",
        "Korea (Democratic People's Republic of)": "KP",
        "Korea, Republic of": "KR",
        "Kuwait": "KW",
        "Cayman Islands": "KY",
        "Kazakhstan": "KZ",
        "Lao People's Democratic Republic": "LA",
        "Lebanon": "LB",
        "Saint Lucia": "LC",
        "Liechtenstein": "LI",
        "Sri Lanka": "LK",
        "Liberia": "LR",
        "Lesotho": "LS",
        "Lithuania": "LT",
        "Luxembourg": "LU",
        "Latvia": "LV",
        "Libya": "LY",
        "Morocco": "MA",
        "Monaco": "MC",
        "Moldova, Republic of": "MD",
        "Montenegro": "ME",
        "Saint Martin (French part)": "MF",
        "Madagascar": "MG",
        "Marshall Islands": "MH",
        "North Macedonia": "MK",
        "Mali": "ML",
        "Myanmar": "MM",
        "Mongolia": "MN",
        "Macao": "MO",
        "Northern Mariana Islands": "MP",
        "Martinique": "MQ",
        "Mauritania": "MR",
        "Montserrat": "MS",
        "Malta": "MT",
        "Mauritius": "MU",
        "Maldives": "MV",
        "Malawi": "MW",
        "Mexico": "MX",
        "Malaysia": "MY",
        "Mozambique": "MZ",
        "Namibia": "NA",
        "New Caledonia": "NC",
        "Niger": "NE",
        "Norfolk Island": "NF",
        "Nigeria": "NG",
        "Nicaragua": "NI",
        "Netherlands": "NL",
        "Norway": "NO",
        "Nepal": "NP",
        "Nauru": "NR",
        "Niue": "NU",
        "New Zealand": "NZ",
        "Oman": "OM",
        "Panama": "PA",
        "Peru": "PE",
        "French Polynesia": "PF",
        "Papua New Guinea": "PG",
        "Philippines": "PH",
        "Pakistan": "PK",
        "Poland": "PL",
        "Saint Pierre and Miquelon": "PM",
        "Pitcairn": "PN",
        "Puerto Rico": "PR",
        "Palestine, State of": "PS",
        "Portugal": "PT",
        "Palau": "PW",
        "Paraguay": "PY",
        "Qatar": "QA",
        "Réunion": "RE",
        "Romania": "RO",
        "Serbia": "RS",
        "Russian Federation": "RU",
        "Rwanda": "RW",
        "Saudi Arabia": "SA",
        "Solomon Islands": "SB",
        "Seychelles": "SC",
        "Sudan": "SD",
        "Sweden": "SE",
        "Singapore": "SG",
        "Saint Helena, Ascension and Tristan da Cunha": "SH",
        "Slovenia": "SI",
        "Svalbard and Jan Mayen": "SJ",
        "Slovakia": "SK",
        "Sierra Leone": "SL",
        "San Marino": "SM",
        "Senegal": "SN",
        "Somalia": "SO",
        "Suriname": "SR",
        "South Sudan": "SS",
        "Sao Tome and Principe": "ST",
        "El Salvador": "SV",
        "Sint Maarten (Dutch part)": "SX",
        "Syrian Arab Republic": "SY",
        "Eswatini": "SZ",
        "Turks and Caicos Islands": "TC",
        "Chad": "TD",
        "French Southern Territories": "TF",
        "Togo": "TG",
        "Thailand": "TH",
        "Tajikistan": "TJ",
        "Tokelau": "TK",
        "Timor-Leste": "TL",
        "Turkmenistan": "TM",
        "Tunisia": "TN",
        "Tonga": "TO",
        "Turkey": "TR",
        "Trinidad and Tobago": "TT",
        "Tuvalu": "TV",
        "Taiwan, Province of China": "TW",
        "Tanzania, United Republic of": "TZ",
        "Ukraine": "UA",
        "Uganda": "UG",
        "United States Minor Outlying Islands": "UM",
        "United States of America": "US",
        "Uruguay": "UY",
        "Uzbekistan": "UZ",
        "Holy See": "VA",
        "Saint Vincent and the Grenadines": "VC",
        "Venezuela (Bolivarian Republic of)": "VE",
        "Virgin Islands (British)": "VG",
        "Virgin Islands (U.S.)": "VI",
        "Viet Nam": "VN",
        "Vanuatu": "VU",
        "Wallis and Futuna": "WF",
        "Samoa": "WS",
        "Yemen": "YE",
        "Mayotte": "YT",
        "South Africa": "ZA",
        "Zambia": "ZM",
        "Zimbabwe": "ZW",
    }
        
    # invert the dictionary: abbrev_to_country = dict(map(reversed, country_to_abbrev.items()))
    cnt = 0
    try:
        for key in country_to_abbrev.keys():
            val = country_to_abbrev[key]
            val = val.lower()
            flag_dir = f"./web-design/flags/{val}.png"
            test_flag_dir = f"../web-design/flags/{val}.png"
            reg_dir_exists = os.path.exists(flag_dir)
            test_dir_exists = os.path.exists(test_flag_dir)
            if (reg_dir_exists or test_dir_exists): 
                if reg_dir_exists:
                    flag = SimpleUploadedFile(name=f'{val}.png', content=open(flag_dir, 'rb').read(), content_type='image/jpeg')
                else:
                    flag = SimpleUploadedFile(name=f'{val}.png', content=open(test_flag_dir, 'rb').read(), content_type='image/jpeg')
                country_FD = {'name':key, 'flag':flag}
                r = DAL.add_instance(some_model=Countries, field_data=country_FD)
                if type(r) is str:
                    raise Exception("Failed to add a country instance within 'populate_countries'.")
                cnt += 1  
            else:
                logger.warning(f"In populate countries, failed at {cnt}/{len(country_to_abbrev)} to add the country where {key = }, since it has no corresponding flag image.")
                return False
        logger.info(f"Successfully added {cnt} countries.")
        return True
    except Exception as e:
        logger.error(f"Failed to populate countries. Failed at {cnt}/{len(country_to_abbrev)}. error: {e}")
        return False
    
