from django.http import HttpResponse, request
from rest_framework import serializers, status
from .models import *
from .dal import DAL
from .validators import *
from .utiles import *
from django.contrib.auth.hashers import make_password
import base64
import logging 
logger = logging.getLogger("pick.me") 


class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = User_Roles
        fields = '__all__'


class ProfileImageBytesField(serializers.Field):

    def to_representation(self, value):
        if value:
            logger.info('profile path = ', str(value.path))
            try:
                path = value.path
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

        return None


class MyOwnUserSerializer(serializers.ModelSerializer):
    thumbnail = ProfileImageBytesField()
    
    class Meta:
        model = Users
        fields =  ['id', 'username', 'password', 'email', 'thumbnail', 'user_role_id']
        # fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    global userFields
    userFields = ['username', 'password', 'email', 'thumbnail', 'user_role_id']
    thumbnail = serializers.ImageField(max_length=None, allow_empty_file=False, allow_null=False, use_url=True, required=False)
    user_role_id = serializers.IntegerField(allow_null=True)

    class Meta:
        model = Users
        fields = userFields
        extra_kwargs = {"username": {"required": False, "allow_null": True},
                        "password": {"required": False, "allow_null": True},
                        "email": {"required": False, "allow_null": True},
                        "thumbnail": {"required": False, "allow_null": True},
                        "user_role_id": {"required": False, "allow_null": True}}

    def validate(self, data):
        partial = False
        data = dict(data) # RTS: Because it's an ordered dict type if there are files attached.
        if 'thumbnail' not in data.keys():
            data['thumbnail'] = SimpleUploadedFile(name='test_image.jpg', content=open("./web-design/static/no_profile.jpg", 'rb').read(), content_type='image/jpg')
        api_request = self.context.get('request')
        id = str(api_request)
        api_method = api_request.method
        if ((api_method == 'PUT') or (api_method == 'PATCH')):
            try:
                id = ''.join(c for c in id if c.isdigit())
                id = int(id)
                data['id'] = id
    
                if (api_method == 'PATCH'):
                    partial = True
                    data['partial'] = True
                    existing_user = DAL.get_instance_by_id(some_model=Users, id=id)
                    if existing_user == str:
                        error_msg = f"PATCH failed. User with {id = } can't be found. Error: {e}"
                        logger.error(error_msg)
                    if 'thumbnail' not in data.keys():
                        data['thumbnail'] = existing_user.thumbnail
               
                    for field in userFields:
                        if (data[field] == None):
                            if field == 'password':
                                val = "pass"
                                data[field] = val
                            elif field == 'user_role_id':
                                val = int(existing_user.user_role.id)
                                data['user_role_id'] = val
                            else:
                                val = getattr(existing_user, field)
                                data[field] = val
                                                        
            except Exception as e:
                error_msg = f"PUT/PATCH failed. Error: {e}"
                logger.error(error_msg)

        bool, result = validate_and_return_userFD(user_field_data=data)
        if not(bool):
            raise serializers.ValidationError(result)
        
        if ((result['password']=="pass") and (partial == True)):
            result['password'] = existing_user.password
        else:
            result['password'] = make_password(str(result['password']))
        
        return result


class CustomerSerializer(serializers.ModelSerializer):

    global customerFields
    customerFields = ['id', 'first_name', 'last_name', 'address', 'phone_no', 'credit_card_no', 'user_id_id']
    user_id_id = serializers.IntegerField(allow_null=True)

    class Meta:
        model = Customers
        fields = customerFields
        extra_kwargs = {"id": {"required": False, "allow_null": True},
                        "first_name": {"required": False, "allow_null": True},
                        "last_name": {"required": False, "allow_null": True},
                        "address": {"required": False, "allow_null": True},
                        "phone_no": {"required": False, "allow_null": True},
                        "credit_card_no": {"required": False, "allow_null": True},
                        "user_id_id": {"required": False, "allow_null": True}}
    

    def validate(self, data):
        partial = False
        data = dict(data) # RTS: Because it's an ordered dict type if there are files attached.
        api_request = self.context.get('request')
        id = str(api_request)
        api_method = api_request.method
        if ((api_method == 'PUT') or (api_method == 'PATCH')):
            try:
                id = ''.join(c for c in id if c.isdigit())
                id = int(id)
                data['id'] = id
                print(f"{id = }")
    
                if (api_method == 'PATCH'):
                    partial = True
                    data['partial'] = True
                    existing_customer = DAL.get_instance_by_id(some_model=Customers, id=id)
                    if existing_customer == str:
                        error_msg = f"PATCH failed. Customer with {id = } can't be found. Error: {e}"
                        logger.error(error_msg)
               
                    for field in customerFields:
                        if (data[field] == None):
                            if field=="user_id_id":
                                val = int(existing_customer.user_id.id)
                                data["user_id_id"] = val
                            else:
                                val = getattr(existing_customer, field)
                                data[field] = val
                                                        
            except Exception as e:
                error_msg = f"PUT/PATCH failed. Error: {e}"
                logger.error(error_msg)


        bool, result = validate_and_return_customerFD(customer_field_data=data)
        if not(bool):
            raise serializers.ValidationError(result)
      
        return result


class AdminSerializer(serializers.ModelSerializer):

    global adminFields
    adminFields = ['id', 'first_name', 'last_name', 'user_id_id']
    user_id_id = serializers.IntegerField(allow_null=True)

    class Meta:
        model = Administrators
        fields = adminFields
        extra_kwargs = {"id": {"required": False, "allow_null": True},
                        "first_name": {"required": False, "allow_null": True},
                        "last_name": {"required": False, "allow_null": True},
                        "user_id_id": {"required": False, "allow_null": True}}
    

    def validate(self, data):
        partial = False
        data = dict(data) # RTS: Because it's an ordered dict type if there are files attached.
        api_request = self.context.get('request')
        id = str(api_request)
        api_method = api_request.method
        if ((api_method == 'PUT') or (api_method == 'PATCH')):
            try:
                id = ''.join(c for c in id if c.isdigit())
                id = int(id)
                data['id'] = id
    
                if (api_method == 'PATCH'):
                    partial = True
                    data['partial'] = True
                    existing_admin = DAL.get_instance_by_id(some_model=Administrators, id=id)
                    if existing_admin == str:
                        error_msg = f"PATCH failed. Administrator with {id = } can't be found. Error: {e}"
                        logger.error(error_msg)
               
                    for field in adminFields:
                        if (data[field] == None):
                            if field=="user_id_id":
                                val = int(existing_admin.user_id.id)
                            else:
                                val = getattr(existing_admin, field)
                            data[field] = val
                     
            except Exception as e:
                error_msg = f"PUT/PATCH failed. Error: {e}"
                logger.error(error_msg)

        bool, result = validate_and_return_adminFD(admin_field_data=data)
        if not(bool):
            raise serializers.ValidationError(result)
      
        return result
    

class DeleteAdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = Administrators
        fields = '__all__'


class FlagImageBytesField(serializers.Field):
    def to_representation(self, value):
        if value:
            logger.info('flag path = ', str(value.path))
            try:
                path = value.path
                split_path = path.split("Airline\\", 1)
                if len(split_path) > 1:
                    new_path = split_path[-1]
                else:
                    new_path = path
                new_path = new_path.replace("\\", "/")
                logger.info('NEW flag path = ', new_path)
                with open(new_path, 'rb') as image_file:
                    image_data = image_file.read()
                    encoded_image = base64.b64encode(image_data).decode('utf-8')
                    return encoded_image

            except Exception as e:
                with open("web-design/static/no_flag.png", 'rb') as image_file:
                    image_data = image_file.read()
                    encoded_image = base64.b64encode(image_data).decode('utf-8')
                    return encoded_image

        return None


class CountrySerializer(serializers.ModelSerializer):
    flag = FlagImageBytesField()

    class Meta:
        model = Countries
        fields = '__all__'
    

class AirlineSerializer(serializers.ModelSerializer):

    global airlineFields
    airlineFields = ['id', 'name', 'country_id_id']
    country_id_id = serializers.IntegerField(allow_null=True)
    id = serializers.IntegerField(allow_null=True, required=False)
   
    class Meta:
        model = Airline_Companies
        fields = airlineFields
        extra_kwargs = {"name": {"required": False, "allow_null": True},
                        "country_id_id": {"required": False, "allow_null": True},
                        "id": {"required": False, "allow_null": True}}
    

    def validate(self, data):
        partial = False
        data = dict(data) 
        print("data = ",data)
        api_request = self.context.get('request')
        id = str(api_request)
        api_method = api_request.method
        if ((api_method == 'PUT') or (api_method == 'PATCH')):
            try:
                id = ''.join(c for c in id if c.isdigit())
                id = int(id)
                data['id'] = id
                if (api_method == 'PATCH'):
                    partial = True
                    data['partial'] = True
                    existing_airline = DAL.get_instance_by_id(some_model=Airline_Companies, id=id)
                    if existing_airline == str:
                        error_msg = f"PATCH failed. Airline company with {id = } can't be found. Error: {e}"
                        logger.error(error_msg)
               
                    for field in airlineFields:
                        if (data[field] == None):

                            if field == 'country_id_id':
                                val = int(existing_airline.country_id.id)
                                data['country_id_id'] = val

                            elif field == 'user_id_id':
                                val = int(existing_airline.user_id.id)
                                data['user_id_id'] = val

                            else:
                                val = getattr(existing_airline, field)
                                data[field] = val
                            
                                                        
            except Exception as e:
                error_msg = f"PUT/PATCH failed. Error: {e}"
                logger.error(error_msg)

     
        bool, result = validate_and_return_airlineFD(airline_field_data=data)
        if not(bool):
            raise serializers.ValidationError(result)
      
        return result
    

class Airline4AdminSerializer(serializers.ModelSerializer):

    global airlineFields
    airlineFields = ['name', 'country_id_id', 'user_id_id']
    user_id_id = serializers.IntegerField(allow_null=True)
    country_id_id = serializers.IntegerField(allow_null=True)

    class Meta:
        model = Airline_Companies
        fields = airlineFields

    def validate(self, data):
        data = dict(data)
 
        bool, result = validate_and_return_airlineFD(airline_field_data=data)
        if not(bool):
            raise serializers.ValidationError(result)
        
        return result
    

class FlightSerializer(serializers.ModelSerializer):

    global flightFields
    flightFields = ['id', 'airline_company_id_id', 'origin_country_id_id', 'destination_country_id_id', 'departure_time', 'landing_time', 'remaining_tickets']
    airline_company_id_id = serializers.IntegerField(allow_null=True)
    origin_country_id_id = serializers.IntegerField(allow_null=True)
    destination_country_id_id = serializers.IntegerField(allow_null=True)

    class Meta:
        model = Flights
        fields = flightFields
        extra_kwargs = {"airline_company_id_id": {"required": False, "allow_null": True},
                        "origin_country_id_id": {"required": False, "allow_null": True},
                        "destination_country_id_id": {"required": False, "allow_null": True},
                        "departure_time": {"required": False, "allow_null": True},
                        "landing_time": {"required": False, "allow_null": True},
                        "remaining_tickets": {"required": False, "allow_null": True},
                        "id": {"required": False, "allow_null": True}}
    

    def validate(self, data):
        partial = False
        data = dict(data) # RTS: Because it's an ordered dict type if there are files attached.
        api_request = self.context.get('request')
        id = str(api_request)
        api_method = api_request.method
        if ((api_method == 'PUT') or (api_method == 'PATCH')):
            try:
                id = ''.join(c for c in id if c.isdigit())
                id = int(id)
                data['id'] = id
    
                if (api_method == 'PATCH'):
                    partial = True
                    data['partial'] = True
                    existing_flight = DAL.get_instance_by_id(some_model=Flights, id=id)
                    if existing_flight == str:
                        error_msg = f"PATCH failed. Flight with {id = } can't be found. Error: {e}"
                        logger.error(error_msg)
               
                    for field in flightFields:
                       
                        if data[field]==None:

                            if field == 'airline_company_id_id':
                                val = int(existing_flight.airline_company_id.id)
                                data['airline_company_id_id'] = val

                            elif field == 'origin_country_id_id':
                                val = int(existing_flight.origin_country_id.id)
                                data['origin_country_id_id'] = val

                            elif field == 'destination_country_id_id':
                                val = int(existing_flight.destination_country_id.id)
                                data['destination_country_id_id'] = val
                            else:
                                val = getattr(existing_flight, field)
                                data[field] = val
                                           
            except Exception as e:
                error_msg = f"PUT/PATCH failed. Error: {e}"
                logger.error(error_msg)

        bool, result = validate_and_return_flightFD(flight_field_data=data)
        if not(bool):
            raise serializers.ValidationError(result)
      
        return result
    


class TicketSerializer(serializers.ModelSerializer):

    global ticketFields
    ticketFields = ['flight_id_id', 'customer_id_id']
    flight_id_id = serializers.IntegerField(allow_null=True)
    customer_id_id = serializers.IntegerField(allow_null=True)

    class Meta:
        model = Tickets
        fields = ticketFields
        extra_kwargs = {"flight_id_id": {"required": False, "allow_null": True},
                        "customer_id_id": {"required": False, "allow_null": True}}
    

    def validate(self, data):
        partial = False
        data = dict(data) # RTS: Because it's an ordered dict type if there are files attached.
        api_request = self.context.get('request')
        id = str(api_request)
        api_method = api_request.method
        if ((api_method == 'PUT') or (api_method == 'PATCH')):
            try:
                id = ''.join(c for c in id if c.isdigit())
                id = int(id)
                data['id'] = id
    
                if (api_method == 'PATCH'):
                    partial = True
                    data['partial'] = True
                    existing_ticket = DAL.get_instance_by_id(some_model=Tickets, id=id)
                    if existing_ticket == str:
                        error_msg = f"PATCH failed. Ticket with {id = } can't be found. Error: {e}"
                        logger.error(error_msg)
               
                    for field in ticketFields:
                        if (data[field] == None):
                            if field == 'flight_id_id':
                                val = int(existing_ticket.flight_id.id)
                                data['flight_id_id'] = val

                            elif field == 'customer_id_id':
                                val = int(existing_ticket.customer_id.id)
                                data['customer_id_id'] = val
                            else:
                                val = getattr(existing_ticket, field)
                                data[field] = val
                
                                                        
            except Exception as e:
                error_msg = f"PUT/PATCH failed. Error: {e}"
                logger.error(error_msg)


        bool, result = validate_and_return_ticketFD(ticket_field_data=data)
        if not(bool):
            raise serializers.ValidationError(result)
      
        return result
    


class SignupSerializer(serializers.ModelSerializer):

    global userFields
    userFields = ['username', 'password', 'email', 'thumbnail']
    thumbnail = serializers.ImageField(max_length=None, allow_empty_file=False, allow_null=False, use_url=True, required=False)
    # user_role_id = serializers.IntegerField()

    class Meta:
        model = Users
        fields = userFields

    def validate(self, data):
        data = dict(data) # RTS: Because it's an ordered dict type if there are files attached.
        if 'thumbnail' not in data.keys():
            data['thumbnail'] = SimpleUploadedFile(name='test_image.jpg', content=open("./web-design/static/no_profile.jpg", 'rb').read(), content_type='image/jpg')
        data['user_role_id'] = 3 # Customer by default
        bool, result = validate_and_return_userFD(user_field_data=data)
        if not(bool):
            raise serializers.ValidationError(result)
        
        result['password'] = make_password(str(result['password']))
        return result


class LoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ['username', 'password']



class MyOwnCustomerSerializer(serializers.ModelSerializer):

    global customerFields
    customerFields = ['first_name', 'last_name', 'address', 'phone_no', 'credit_card_no']

    class Meta:
        model = Customers
        fields = customerFields
        extra_kwargs = {"first_name": {"required": False, "allow_null": True},
                        "last_name": {"required": False, "allow_null": True},
                        "address": {"required": False, "allow_null": True},
                        "phone_no": {"required": False, "allow_null": True},
                        "credit_card_no": {"required": False, "allow_null": True}}
    
    def validate(self, data):
        data = dict(data)
        context = self.context
        id = int(context['pk'])
        data['partial'] = True
        data['id'] = id
        try:
            existing_customer = DAL.get_instance_by_id(some_model=Customers, id=id)
            if existing_customer == str:
                error_msg = f"PATCH failed. Customer with {id = } can't be found. Error: {e}"
                logger.error(error_msg)
        
            data['user_id_id'] = int(existing_customer.user_id.id)
            for field in customerFields:
                if ((data[field] == None)):
                    if hasattr(existing_customer, field):
                        val = getattr(existing_customer, field)
                        data[field] = val
                                                    
        except Exception as e:
            error_msg = f"PUT/PATCH failed. Error: {e}"
            logger.error(error_msg)


        bool, result = validate_and_return_customerFD(customer_field_data=data)
        if not(bool):
            raise serializers.ValidationError(result)
        result.pop('partial')
        result.pop('id')
        return result
    

class Ticket4CustomerSerializer(serializers.ModelSerializer):

    flight_id_id = serializers.IntegerField()

    class Meta:
        model = Tickets
        fields = ['flight_id_id']    

    def validate(self, data):
        data = dict(data)
        context = self.context
        customer_id = int(context['customer_id'])
        data['customer_id_id'] = customer_id
        logger.info(f"{data = }")
        bool, result = validate_and_return_ticketFD(ticket_field_data=data)
        if not(bool):
            raise serializers.ValidationError(result)
      
        return result



class MyOwnAirlineSerializer(serializers.ModelSerializer):

    global airlineFields
    airlineFields = ['name', 'country_id_id']
    country_id_id = serializers.IntegerField(allow_null=True, required=False)
   
    class Meta:
        model = Airline_Companies
        fields = airlineFields
        extra_kwargs = {"name": {"required": False, "allow_null": True},
                        "country_id_id": {"required": False, "allow_null": True}}
    

    def validate(self, data):
        data = dict(data)
        context = self.context
        id = int(context['pk'])
        data['partial'] = True
        data['id'] = id
        # logger.info("my airline api data = ",data)
        try:
            existing_airline = DAL.get_instance_by_id(some_model=Airline_Companies, id=id)
            if existing_airline == str:
                error_msg = f"PATCH failed. Airline company with {id = } can't be found. Error: {e}"
                logger.error(error_msg)
        
            data['user_id_id'] = int(existing_airline.user_id.id)
            for field in airlineFields:
                if ((data[field] == None)):
                    if hasattr(existing_airline, field):
                        val = getattr(existing_airline, field)
                        data[field] = val
                                                    
        except Exception as e:
            error_msg = f"PUT/PATCH failed. Error: {e}"
            logger.error(error_msg)


        bool, result = validate_and_return_airlineFD(airline_field_data=data)
        logger.info("Sent!!")
        if not(bool):
            raise serializers.ValidationError(result)
      
        result.pop('partial')
        result.pop('id')
        return result



class Flight4AirlineSerializer(serializers.ModelSerializer):

    global flightFields
    flightFields = ['origin_country_id_id', 'destination_country_id_id', 'departure_time', 'landing_time', 'remaining_tickets']
    origin_country_id_id = serializers.IntegerField(allow_null=True, required=False)
    destination_country_id_id = serializers.IntegerField(allow_null=True, required=False)

    class Meta:
        model = Flights
        fields = flightFields
        extra_kwargs = {"origin_country_id_id": {"required": False, "allow_null": True},
                        "destination_country_id_id": {"required": False, "allow_null": True},
                        "departure_time": {"required": False, "allow_null": True},
                        "landing_time": {"required": False, "allow_null": True},
                        "remaining_tickets": {"required": False, "allow_null": True}}
    

    def validate(self, data):

        data = dict(data)
        context = self.context
        id = int(context['pk'])
        data['partial'] = True
        data['id'] = id
        try:
            existing_flight = DAL.get_instance_by_id(some_model=Flights, id=id)
            if existing_flight == str:
                error_msg = f"PATCH failed. Flight with {id = } can't be found. Error: {e}"
                logger.error(error_msg)
        
            data['airline_company_id_id'] = int(existing_flight.airline_company_id.id)
            logger.info(f"got this : {data = }")
            for field in flightFields:
                if ((data[field] == None)):
                    if field == 'origin_country_id_id':
                        val = int(existing_flight.origin_country_id.id)
                        data['origin_country_id_id'] = val

                    elif field == 'destination_country_id_id':
                        val = int(existing_flight.destination_country_id.id)
                        data['destination_country_id_id'] = val
                    else:
                        val = getattr(existing_flight, field)
                        data[field] = val
                                                    
        except Exception as e:
            error_msg = f"PUT/PATCH failed. Error: {e}"
            logger.error(error_msg)


        bool, result = validate_and_return_flightFD(flight_field_data=data)
        if not(bool):
            raise serializers.ValidationError(result)
      
        result.pop('partial')
        result.pop('id')
        return result



class AddFlight4AirlineSerializer(serializers.ModelSerializer):

    global flightFields
    flightFields = ['origin_country_id_id', 'destination_country_id_id', 'departure_time', 'landing_time', 'remaining_tickets']
    origin_country_id_id = serializers.IntegerField()
    destination_country_id_id = serializers.IntegerField()
    departure_time = serializers.DateTimeField()
    landing_time = serializers.DateTimeField()

    class Meta:
        model = Flights
        fields = flightFields

    def validate(self, data):
        data = dict(data)
        print(f"here inside {data = }")
        context = self.context
        data['airline_company_id_id'] = int(context['airline_id'])

        bool, result = validate_and_return_flightFD(flight_field_data=data)
        if not(bool):
            raise serializers.ValidationError(result)
      
        return result
    

class FlightParametersSerializer(serializers.Serializer):

    global flightFields
    flightFields = ['origin_country_id_id', 'destination_country_id_id', 'departure_time', 'landing_time', 'remaining_tickets']
    origin_country_id_id = serializers.IntegerField(allow_null=True, required=False)
    destination_country_id_id = serializers.IntegerField(allow_null=True, required=False)
    departure_time = serializers.DateTimeField(allow_null=True, required=False)
    landing_time = serializers.DateTimeField(allow_null=True, required=False)
    remaining_tickets = serializers.IntegerField(allow_null=True, required=False)
    airline_company_id_id = serializers.IntegerField(allow_null=True, required=False)

    class Meta:
        extra_kwargs = {"origin_country_id_id": {"required": False, "allow_null": True},
                        "destination_country_id_id": {"required": False, "allow_null": True},
                        "departure_time": {"required": False, "allow_null": True},
                        "landing_time": {"required": False, "allow_null": True},
                        "remaining_tickets": {"required": False, "allow_null": True},
                        "airline_company_id_id": {"required": False, "allow_null": True}}

    def validate(self, data):
        data = dict(data)
        filters = {}
        for key, value in data.items():
            filters[key] = value
        return filters
    


class FlightParametersSerializerA(serializers.Serializer):

    flightFields = ['airline_company', 'origin_country', 'destination_country', 'departure_time', 'landing_time', 'remaining_tickets']
    origin_country = serializers.CharField(allow_null=True, required=False)
    destination_country = serializers.CharField(allow_null=True, required=False)
    departure_time = serializers.DateTimeField(allow_null=True, required=False)
    landing_time = serializers.DateTimeField(allow_null=True, required=False)
    remaining_tickets = serializers.IntegerField(allow_null=True, required=False)
    airline_company = serializers.CharField(allow_null=True, required=False)

    class Meta:
        extra_kwargs = {
                        "airline_company": {"required": False, "allow_null": True},
                        "origin_country": {"required": False, "allow_null": True},
                        "destination_country": {"required": False, "allow_null": True},
                        "departure_time": {"required": False, "allow_null": True},
                        "landing_time": {"required": False, "allow_null": True},
                        "remaining_tickets": {"required": False, "allow_null": True}}

    def validate(self, data):
        data = dict(data)
        filters = {}
        for key, value in data.items():
            filters[key] = value
        return filters
    


class AirlineParametersSerializer(serializers.Serializer):

    global airlineFields
    airlineFields = ['name', 'country_id_id']
    country_id_id = serializers.IntegerField(allow_null=True, required=False)
    name = serializers.CharField(allow_null=True, required=False)
   
    class Meta:
        extra_kwargs = {"name": {"required": False, "allow_null": True},
                        "country_id_id": {"required": False, "allow_null": True}}
    

    def validate(self, data):
        data = dict(data)
        filters = {}
        for key, value in data.items():
            filters[key] = value
        return filters
    

class ShowFlightSerializer(serializers.ModelSerializer):
    airline_company = serializers.SerializerMethodField()
    origin_country = serializers.SerializerMethodField()
    destination_country = serializers.SerializerMethodField()

    def get_airline_company(self, obj):
        airline_id = obj.airline_company_id.id
        val = DAL.get_name_by_id(some_model=Airline_Companies, id=airline_id)
        return val
    
    def get_origin_country(self, obj):
        country_id = obj.origin_country_id.id
        val = DAL.get_name_by_id(some_model=Countries, id=country_id)
        return val
    
    def get_destination_country(self, obj):
        country_id = obj.destination_country_id.id
        val = DAL.get_name_by_id(some_model=Countries, id=country_id)
        return val

    class Meta:
        model = Flights  
        fields = ['id', 'airline_company', 'origin_country', 'destination_country', 'departure_time', 'landing_time', 'remaining_tickets']
    


class UsernameSerializer(serializers.Serializer):

    username = serializers.CharField(required=True)



class NameSerializer(serializers.Serializer):

    model = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
