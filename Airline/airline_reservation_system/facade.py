from . import dal 
from .utiles import update_role_session, val_up_customer, val_add_customer
from datetime import datetime
from .models import *
from .validators import *
from abc import ABC, abstractmethod
from django.contrib.auth.models import update_last_login
from django.contrib.auth import login, authenticate, logout
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import update_last_login
from django.http import request
from django.views.decorators.csrf import csrf_exempt
import logging 
logger = logging.getLogger("pick.me") 


class Facade_Base(ABC):

    @staticmethod
    def get_all_flights():
        flights = dal.DAL.get_all_instances(some_model=Flights)                                                                             
        return flights

    @staticmethod
    def get_flight_by_id(flight_id:int):
        if not(validate_id(id=flight_id)):
            error_msg = f"Failed to get a flight. id = {id}, can't be found."
            logger.error(error_msg)
            return error_msg
        flight = dal.DAL.get_instance_by_id(some_model=Flights, id=flight_id)                                                          
        return flight

    @staticmethod
    def get_flights_by_parameters_Static(origin_country_id:int, destination_country_id:int, date:datetime.date):
        flights = dal.get_flights_by_parameters_S(origin_country_id=origin_country_id, 
                                                destination_country_id=destination_country_id,
                                                date=date)   
        return flights

    @staticmethod
    def get_flights_by_parameters_Dynamic(filters:dict):
        failed = False
        flights = dal.get_flights_by_parameters_D(filters=filters)
        if type(flights)==str:
            failed = True
        return failed, flights
    
    @staticmethod
    def get_all_airlines():
        airlines = dal.DAL.get_all_instances(some_model=Airline_Companies)                                                                             
        return airlines

    @staticmethod
    def get_airline_by_id(airline_id:int):
        if not(validate_id(id=airline_id)):
            error_msg = f"Failed to get an airline company by id. airline_id = {airline_id}, can't be found."
            logger.error(error_msg)
            return error_msg
        airline = dal.DAL.get_instance_by_id(some_model=Airline_Companies, id=airline_id)                                                          
        return airline

    @staticmethod
    def get_airlines_by_parameters_Static(name:str, country_id:int, user_id:int):
        airlines = dal.get_airlines_by_parameters_S(name=name,
                                                  country_id=country_id,
                                                  user_id=user_id)   
        return airlines

    @staticmethod
    def get_airlines_by_parameters_Dynamic(filters:dict):
        failed = False
        airlines = dal.get_airlines_by_parameters_D(filters=filters)
        if type(airlines)==str:
            failed = True
        return failed, airlines
    
    @staticmethod
    def get_all_countries():
        countries = dal.DAL.get_all_instances(some_model=Countries)                                                                             
        return countries

    @staticmethod
    def get_country_by_id(country_id:int):
        if not(validate_id(id=country_id)):
            error_msg = f"Failed to get a country by id. country_id = {country_id}, can't be found."
            logger.error(error_msg)
            return error_msg
        country = dal.DAL.get_instance_by_id(some_model=Countries, id=country_id)                                                          
        return country
    
    @staticmethod
    def create_new_user(user_FD:dict):
        if (type(user_FD) != dict):
            error_msg = f"Failed to add a user. Bad input. 'user_FD' must be a dictionary."
            logger.error(error_msg)
            return False
        if not(validate_b4_add(some_model=Users, field_data=user_FD)):
            error_msg = f"Failed to add a user. Bad input. Failed to validate a user's data. 'user_FD[0]' = {user_FD[0]}."
            logger.error(error_msg)
            return False
        if (type(dal.DAL.add_instance(some_model=Users, field_data=user_FD)) == str):
            error_msg = f"Failed to add a user. 'user_FD[0]' = {user_FD[0]}."
            logger.error(error_msg)
            return False
        return True 
    
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
                        instances = some_model.objects.filter(first_name__icontains=name)
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


class Anonymous_Facade(Facade_Base):

    @staticmethod
    def login_user(request:request ,username:str, password:str):
        """
        logs in user. Stores their role_name and token key in session.
        Upon failure returns False and an error message.
        Upon success returns the role_name str and the token_key str.
        """
        username = str(username)
        password = str(password)

        user = authenticate(username=username, password=password)
        if user is None:
            err_msg = "Login Failed. Invalid user login credentials. Try again."
            logger.error(err_msg)
            return False, err_msg

        login(request=request, user=user)
        token, created = Token.objects.get_or_create(user=user)
        token_key = token.key 
        request.session['user_token'] = token_key

        user_id = user.id
        bool, role_or_err = update_role_session(request=request, user_id=user_id)
        if bool==False:
            err_msg = f"Login Failed. Could not update the session's role name value. Error: {role_or_err}"
            logger.error(err_msg)
            return False, err_msg
        
        request.session['user_id'] = user_id
        
        logger.info(f"User {username = }, has logged in successfully. Their current token is: {token_key}. Their role name is: {role_or_err}.")
        return role_or_err, token_key
    
    @staticmethod
    def logout_user(request:request):
        """
        logs out the logged in user.
        """
        request.session.flush() #deletes all the session data
        logout(request)
        msg = "You have successfully logged out."
        return msg
    
    @staticmethod
    def add_customer(customer_FD:dict):
        if (type(customer_FD) != dict):
            error_msg = f"Failed to add a customer. Bad input. 'customer_FD' must be a dictionary."
            logger.error(error_msg)
            return False
        if not(validate_b4_add(some_model=Customers, field_data=customer_FD)):
            error_msg = f"Failed to add a customer. Bad input. Failed to validate a customer's data. 'customer_FD[0]' = {customer_FD[0]}."
            logger.error(error_msg)
            return False
        if (type(dal.DAL.add_instance(some_model=Customers, field_data=customer_FD)) == str):
            error_msg = f"Failed to add a customer. 'customer_FD[0]' = {customer_FD[0]}."
            logger.error(error_msg)
            return False
        return True 


class Customer_Facade(Anonymous_Facade):

    @staticmethod
    def update_customer(customer_FD:dict, instance:Customers):

        if (type(customer_FD) != dict):
            error_msg = f"Failed to update a customer. Bad input. 'customer_FD' must be a dictionary."
            logger.error(error_msg)
            return False
     
        if not(val_up_customer(customer_field_data=customer_FD, instance=instance)):
            error_msg = f"Failed to update a customer. 'customer_FD[0]' = {customer_FD[0]}."
            logger.error(error_msg)
            return False
        return True 

    @staticmethod
    def add_ticket(ticket_FD:dict):
        if (type(ticket_FD) != dict):
            error_msg = f"Failed to add a ticket. Bad input. 'ticket_FD' must be a dictionary."
            logger.error(error_msg)
            return False
        if not(validate_b4_add(some_model=Tickets, field_data=ticket_FD)):
            error_msg = f"Failed to add a ticket. Bad input. Failed to validate a ticket's data. 'ticket_FD[0]' = {ticket_FD[0]}."
            logger.error(error_msg)
            return False
        if (type(dal.DAL.add_instance(some_model=Tickets, field_data=ticket_FD)) == str):
            error_msg = f"Failed to add a ticket. 'ticket_FD[0]' = {ticket_FD[0]}."
            logger.error(error_msg)
            return False
        return True 
    
    @staticmethod
    def remove_ticket(instance:Tickets):

        if not(validate_instance_type(some_model=Tickets, instance=instance)):
            error_msg = f"Failed to remove a ticket. Bad input. 'instance' is not an instance of Tickets."
            logger.error(error_msg)
            return error_msg
        
        id = DAL.get_id_from_instance(instance=instance)
        if not(type(id) == int):
            error_msg = f"Failed to remove a ticket. Bad input. Couldn't get the id of the ticket instance."
            logger.error(error_msg)
            return error_msg
        
        bool, msg = dal.DAL.remove_instance(some_model=Tickets, instance=instance)
        if not(bool):
            error_msg = f"Failed to remove a ticket. id = {id}."
            logger.error(error_msg)
            return msg
        
        return msg 
    
    @staticmethod
    def get_my_tickets():
        """
        The tickets of the logged in customer.
        NTS: DO auth first. Save the token globally.
        """

        """
        fetch the logged in customer's id here.
        """

        try:
            id = int(id)
            tickets = Tickets.objects.filter(customer_id=id)
            logger.info(f"Succeeded to find the tickets of the customer whose id is {id}.")
            return tickets
        except Exception as e:
            err_msg = f"Failed to find the tickets of the customer whose id is {id}. {e}"
            logger.error(err_msg)
            return err_msg

class Airline_Facade(Anonymous_Facade):

    @staticmethod
    def get_my_flights():
        """
        Returns the flights of the logged in airline company.
        NTS: DO auth first. Save the token globally.
        """

        """
        fetch the logged in customer's id here.
        """

        try:
            id = int(id)
            flights = Tickets.objects.filter(customer_id=id)
            logger.info(f"Successfully got the flights of the airline company with id = {id}.")
            return flights
        except Exception as e:
            err_msg = f"Failed to get the flights of the airline company with id = {id}. {e}"
            logger.error(err_msg)
            return err_msg

    @staticmethod  
    def update_airline(airline_FD:dict, instance:Airline_Companies):

        if (type(airline_FD) != dict):
            error_msg = f"Failed to update an airline company. Bad input. 'airline_FD' must be a dictionary."
            logger.error(error_msg)
            return error_msg
     
        if not(validate_b4_update(some_model=Airline_Companies, field_data=airline_FD, instance=instance)):
            error_msg = f"Failed to update an airline company. 'airline_FD[0]' = {airline_FD[0]}."
            logger.error(error_msg)
            return error_msg
        
        if (type(DAL.update_instance(some_model=Airline_Companies ,field_data=airline_FD, instance=instance)) == str):
            error_msg = f"Failed to update an airline company. 'airline_FD[0]' = {airline_FD[0]}."
            logger.error(error_msg)
            return error_msg
        return True 

    @staticmethod
    def add_flight(flight_FD:dict):
        if (type(flight_FD) != dict):
            error_msg = f"Failed to add a flight. Bad input. 'flight_FD' must be a dictionary."
            logger.error(error_msg)
            return False
        if not(validate_b4_add(some_model=Flights, field_data=flight_FD)):
            error_msg = f"Failed to add a flight. Bad input. Failed to validate a flight's data. 'flight_FD[0]' = {flight_FD[0]}."
            logger.error(error_msg)
            return False
        if (type(dal.DAL.add_instance(some_model=Flights, field_data=flight_FD)) == str):
            error_msg = f"Failed to add a flight. 'flight_FD[0]' = {flight_FD[0]}."
            logger.error(error_msg)
            return False
        return True 

    @staticmethod  
    def update_flight(flight_FD:dict, instance:Flights):

        if (type(flight_FD) != dict):
            error_msg = f"Failed to update a flight. Bad input. 'flight_FD' must be a dictionary."
            logger.error(error_msg)
            return error_msg
     
        if not(validate_b4_update(some_model=Flights, field_data=flight_FD, instance=instance)):
            error_msg = f"Failed to update a flight. 'flight_FD[0]' = {flight_FD[0]}."
            logger.error(error_msg)
            return error_msg
        
        if (type(DAL.update_instance(some_model=Flights ,field_data=flight_FD, instance=instance)) == str):
            error_msg = f"Failed to update a flight. 'flight_FD[0]' = {flight_FD[0]}."
            logger.error(error_msg)
            return error_msg
        return True 
    
    @staticmethod
    def remove_flight(instance:Flights):

        if not(validate_instance_type(some_model=Flights, instance=instance)):
            error_msg = f"Failed to remove a flight. Bad input. 'instance' is not an instance of Flights."
            logger.error(error_msg)
            return error_msg
        
        id = DAL.get_id_from_instance(instance=instance)
        if not(type(id) == int):
            error_msg = f"Failed to remove a flight. Bad input. Couldn't get the id of the Flights instance."
            logger.error(error_msg)
            return error_msg
        
        bool, msg = dal.DAL.remove_instance(some_model=Flights, instance=instance)
        if not(bool):
            error_msg = f"Failed to remove a flight. id = {id}."
            logger.error(error_msg)
            return msg
        
        return msg 


class Administrator_Facade(Anonymous_Facade):
    
    @staticmethod
    def get_all_customers():
        customers = dal.DAL.get_all_instances(some_model=Customers)                                                                             
        return customers
    
    @staticmethod
    def add_airline(airline_FD:dict):
        if (type(airline_FD) != dict):
            error_msg = f"Failed to add an airline company. Bad input. 'airline_FD' must be a dictionary."
            logger.error(error_msg)
            return False
        if not(validate_b4_add(some_model=Airline_Companies, field_data=airline_FD)):
            error_msg = f"Failed to add an airline company. Bad input. Failed to validate an airline company's data. 'airline_FD[0]' = {airline_FD[0]}."
            logger.error(error_msg)
            return False
        if (type(dal.DAL.add_instance(some_model=Airline_Companies, field_data=airline_FD)) == str):
            error_msg = f"Failed to add an airline company. 'airline_FD[0]' = {airline_FD[0]}."
            logger.error(error_msg)
            return False
        return True 
    
    @staticmethod
    def add_customer(customer_FD:dict):

        if (type(customer_FD) != dict):
            error_msg = f"Failed to add a customer. Bad input. 'customer_FD' must be a dictionary."
            logger.error(error_msg)
            return False
     
        if not(val_add_customer(customer_field_data=customer_FD)):
            error_msg = f"Failed to add a customer. 'customer_FD[0]' = {customer_FD[0]}."
            logger.error(error_msg)
            return False
        return True 
    
    @staticmethod
    def add_admin(admin_FD:dict):
        if (type(admin_FD) != dict):
            error_msg = f"Failed to add an administrator. Bad input. 'admin_FD' must be a dictionary."
            logger.error(error_msg)
            return False
        if not(validate_b4_add(some_model=Administrators, field_data=admin_FD)):
            error_msg = f"Failed to add an administrator. Bad input. Failed to validate an administrator's data. 'admin_FD[0]' = {admin_FD[0]}."
            logger.error(error_msg)
            return False
        if (type(dal.DAL.add_instance(some_model=Administrators, field_data=admin_FD)) == str):
            error_msg = f"Failed to add an administrator. 'admin_FD[0]' = {admin_FD[0]}."
            logger.error(error_msg)
            return False
        return True 
    
    @staticmethod
    def remove_airline(instance:Airline_Companies):

        if not(validate_instance_type(some_model=Airline_Companies, instance=instance)):
            error_msg = f"Failed to remove an airline company. Bad input. 'instance' is not an instance of Airline_Companies."
            logger.error(error_msg)
            return error_msg
        
        id = DAL.get_id_from_instance(instance=instance)
        if not(type(id) == int):
            error_msg = f"Failed to remove an airline company. Bad input. Couldn't get the id of the Airline_Companies instance."
            logger.error(error_msg)
            return error_msg
        
        bool, msg = dal.DAL.remove_instance(some_model=Airline_Companies, instance=instance)
        if not(bool):
            error_msg = f"Failed to remove an airline company. id = {id}."
            logger.error(error_msg)
            return msg
        
        return msg 
    
    @staticmethod
    def remove_customer(instance:Customers):

        if not(validate_instance_type(some_model=Customers, instance=instance)):
            error_msg = f"Failed to remove a customer. Bad input. 'instance' is not an instance of Customers."
            logger.error(error_msg)
            return error_msg
        
        id = DAL.get_id_from_instance(instance=instance)
        if not(type(id) == int):
            error_msg = f"Failed to remove a customer. Bad input. Couldn't get the id of the Customers instance."
            logger.error(error_msg)
            return error_msg
        
        bool, msg = dal.DAL.remove_instance(some_model=Customers, instance=instance)
        if not(bool):
            error_msg = f"Failed to remove a customer. id = {id}."
            logger.error(error_msg)
            return msg
        
        return msg 
    
    @staticmethod
    def remove_admin(instance:Administrators): # what happens when an admin removes themselves? --> send success msg & revoke their permissions to fit the anonymous status.

        current_user_id = 0  # fetch it here from session or whatever

        if not(validate_instance_type(some_model=Administrators, instance=instance)):
            error_msg = f"Failed to remove an administrator. Bad input. 'instance' is not an instance of Administrators."
            logger.error(error_msg)
            return error_msg
        
        id = DAL.get_id_from_instance(instance=instance)
        if not(type(id) == int):
            error_msg = f"Failed to remove an administrator. Bad input. Couldn't get the id of the Administrators instance."
            logger.error(error_msg)
            return error_msg
                
        bool, msg = dal.DAL.remove_instance(some_model=Administrators, instance=instance)
        if not(bool):
            error_msg = f"Failed to remove an administrator. id = {id}."
            logger.error(error_msg)
            return msg
        
        if (id == current_user_id):
            return msg, Anonymous_Facade
        return msg 
    
    @staticmethod
    def get_userID_by_username(username:str):
        if not (Users.objects.filter(username=username).exists()):
            return 0
        userID =  Users.objects.get(username=username).id
        return userID