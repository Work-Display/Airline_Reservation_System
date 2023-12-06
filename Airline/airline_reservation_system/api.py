from .models import *
from .facade import *
from .dal import *
from .utiles import prepare_profile
from .serializers import *
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from django.contrib.auth.models import update_last_login
from django.contrib.auth import logout
from .decorators import *
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict
import logging 
logger = logging.getLogger("pick.me") 

# COPY: @allowed_roles(['Administrator', 'Airline Company', 'Customer'])

# ModelViewSets: =============================================================================================================================

# @allowed_roles(['Administrator']) # Equal to this v
@method_decorator(allowed_roles(['Administrator']), name='dispatch')
class Role4AdminViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows User_Roles to be viewed.
    """
    queryset = User_Roles.objects.all().order_by('role_name')
    serializer_class = RoleSerializer
    # permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get']


class MyOwnUserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that returns the logged in user object. It is for system use, but it's open for everyone. 'List' and 'Retrieve' act the same. (Couldn't enable only list).
    """
    queryset = Users.objects.all().order_by('id')
    serializer_class = MyOwnUserSerializer
    http_method_names = ['get']

    def list(self, request):
        user_id = get_user_id_from_session(request=request)
        if (type(user_id)!=int):
            err_msg = f"You are not logged in."
            return Response(err_msg, status=status.HTTP_404_NOT_FOUND)
    
        user = Users.objects.get(id=user_id)
        logger.info(f"1 {user = }")

        profile = prepare_profile(user.thumbnail)
    
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'user_role': user.user_role.role_name,
            'thumbnail': profile
        }
        return Response(user_data, status=status.HTTP_200_OK)

       
    def retrieve(self, request, pk):
        user_id = get_user_id_from_session(request=request)
        if (type(user_id)!=int):
            err_msg = f"You are not logged in."
            return Response(err_msg, status=status.HTTP_404_NOT_FOUND)
    
        user = Users.objects.get(id=user_id)
        logger.info(f"1 {user = }")

        profile = prepare_profile(user.thumbnail)
    
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'user_role': user.user_role.role_name,
            'thumbnail': profile
        }
        return Response(user_data, status=status.HTTP_200_OK)


@method_decorator(allowed_roles(['Administrator']), name='dispatch')
class User4AdminViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Users to be viewed or edited.
    """
    queryset = Users.objects.all().order_by('id')
    serializer_class = UserSerializer


@method_decorator(allowed_roles(['Administrator']), name='dispatch')
class Customer4AdminViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Customers to be viewed or edited.
    """
    queryset = Customers.objects.all().order_by('id')
    serializer_class = CustomerSerializer

    def destroy(self, request, *args, **kwargs):
        pk = int(kwargs['pk'])
        requested_customer = Customers.objects.filter(id=pk).exists()
        if not requested_customer:
            err_msg = f"Bad input. Your requested customer with id = {pk} doesn't exist."
            logger.error(err_msg)
            return Response(err_msg, status=status.HTTP_404_NOT_FOUND)
        customer = Customers.objects.get(id=pk)

        tickets = get_tickets_by_customer(customer_id=pk)
        if (type(tickets)==str):
            customer.delete()
            info_msg = f"Customer with id = {pk}, doesn't own any tickets. They got successfully deleted."
            logger.info(info_msg)
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        for ticket in tickets:
           flight = Flights.objects.get(id=ticket.flight_id.id)
           ticket.delete()
           flight.remaining_tickets += 1
           flight.save()
             
        customer.delete()
        info_msg = f"Customer with id = {pk}, does own tickets. {tickets = }. The customer and their tickets were successfully deleted."
        logger.info(info_msg)
        return Response(status=status.HTTP_204_NO_CONTENT)

    

@method_decorator(allowed_roles(['Customer']), name='dispatch')
class Customer4CustomerUserAdd(viewsets.ModelViewSet):
    """
    API endpoint that allows Users with Customer user roles to register themselves in the Customers table.
    """
    queryset = Customers.objects.all().order_by('id')
    serializer_class = MyOwnCustomerSerializer
    http_method_names = ["post"]

    def create(self, request, *args, **kwargs):
        user_id = get_user_id_from_session(request=request)
        if (type(user_id)!=int):
            err_msg = f"Error! Failed to get 'user_id' from session and so couldn't check if you have a permission to view this page."
            logger.error(err_msg)
            return Response(err_msg, status=status.HTTP_403_FORBIDDEN)
        
        already_customer = Customers.objects.filter(user_id_id=user_id).exists()
        if already_customer:
            already_customer = Customers.objects.get(user_id_id=user_id)
            customer_id = already_customer.id
            customer_name = already_customer.first_name
            err_msg = f"You are already registered as a customer {customer_name}, your customer id is: {customer_id}."
            logger.error(err_msg)
            return Response(err_msg, status=status.HTTP_403_FORBIDDEN)
        
        customer_FD = dict(request.data)
        logger.info(f"{customer_FD = }")
        
        tmp = ''
        for k, v in customer_FD.items():
            if (v == ['']):
                customer_FD[k] = None
            else:
                tmp = str(customer_FD[k][0])
                logger.info(f"{tmp = }")
                customer_FD[k] = tmp
                if tmp.isnumeric():
                    customer_FD[k] = int(tmp)

        customer_FD['user_id_id'] = user_id
        logger.info(f"In become customer, sending this for validation: {customer_FD = }")
        bool, result = validate_and_return_customerFD(customer_field_data=customer_FD)
        if not(bool):
            logger.error(f"Become a customer failed. Validation error: {result}")
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        
        add_result = DAL.add_instance(some_model=Customers, field_data=result)
        if (type(add_result) == str):
            error_msg = f"Failed to add a customer. customer_FD = {result}. Error: {add_result = }"
            logger.error(error_msg)
            return Response(error_msg, status=status.HTTP_400_BAD_REQUEST)
        
        info_msg = f"Successfully validated and added a customer in become-a-customer. {user_id = }"
        logger.info(info_msg)
        customer = Customers.objects.get(user_id_id = user_id)
        customer = model_to_dict(customer)
        return Response(customer, status=status.HTTP_200_OK)
 


@method_decorator(allowed_roles(['Administrator']), name='dispatch')
class Admin4AdminViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Administrators to be viewed or edited.
    """
    queryset = Administrators.objects.all().order_by('id')
    serializer_class = AdminSerializer
    http_method_names = ["get", "post", "put", "patch"]



@method_decorator(allowed_roles(['Administrator']), name='dispatch')
class DeleteAdminViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Administrators to delete themselves. WARNING: this doesn't only deletes the admin's instance in the Administrators table, it also deletes the admin's USER.
    """
    queryset = Administrators.objects.all().order_by('id')
    serializer_class = DeleteAdminSerializer
    http_method_names = ["delete"]

    def destroy(self, request, *args, **kwargs):
        pk = int(kwargs['pk'])
        user_id = get_user_id_from_session(request=request)
        if (type(user_id)!=int):
            err_msg = f"Error! Failed to get 'user_id' from session and so couldn't check if you have a permission to view this page."
            logger.error(err_msg)
            return Response(err_msg, status=status.HTTP_403_FORBIDDEN)
    
        requested_admin = Administrators.objects.filter(id=pk).exists()
        if not requested_admin:
            err_msg = f"Bad input. Your requested admin account id = {pk} doesn't exist."
            logger.error(err_msg)
            return Response(err_msg, status=status.HTTP_404_NOT_FOUND)
        requested_admin = Administrators.objects.get(id=pk)
        req_admin_id = requested_admin.id

        requesting_admin = Administrators.objects.filter(user_id=user_id).exists()
        if not requesting_admin:
            err_msg = f"You can't access delete admin yet, because you still haven't added yourself as an admin. Having an admin user role isn't enough. Your user id: {user_id}."
            logger.error(err_msg)
            return Response(err_msg, status=status.HTTP_404_NOT_FOUND)
        admin = Administrators.objects.get(user_id=user_id)
        admin_id = admin.id
        if (admin_id != int(pk)):
            err_msg = f"Sorry, but you are forbidden from deleting admin accounts other than your own. Your admin account id = {admin_id}. Requested pk = {req_admin_id}. Your admin account id and your requested pk should match."
            logger.error(err_msg)
            return Response(err_msg, status=status.HTTP_403_FORBIDDEN)
        

        logout(request=request)
        admin.delete()
        user_token = Token.objects.get(user_id=user_id)
        user_token.delete()
        user = Users.objects.get(id=user_id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@method_decorator(allowed_roles(['Administrator']), name='dispatch')
class Airline4AdminViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Airline_Companies to be added or removed by admins.
    """
    queryset = Airline_Companies.objects.all().order_by('id')
    serializer_class = Airline4AdminSerializer
    http_method_names = ["post", "delete"]

    def destroy(self, request, *args, **kwargs):
        pk = int(kwargs['pk'])
        requested_airline = Airline_Companies.objects.filter(id=pk).exists()
        if not requested_airline:
            err_msg = f"Bad input. Your requested airline company with id = {pk} doesn't exist."
            logger.error(err_msg)
            return Response(err_msg, status=status.HTTP_404_NOT_FOUND)
        airline = Airline_Companies.objects.get(id=pk)

        flights = get_flights_by_airlineID(airline_id=pk)
        if (type(flights)==str):
            info_msg = f"Airline company with id = {pk}, doesn't have any flights. It got successfully deleted."
            logger.info(info_msg)
            airline.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        
        for flight in flights:
            flight_id = flight.id
            related_tickets = Tickets.objects.filter(flight_id_id = flight_id).exists()
            if not related_tickets:
                flight.delete()
                info_msg = f"In delete airline pk = {pk}, flight with id = {flight_id} has been successfully deleted."
                logger.info(info_msg)
            else: 
                related_tickets = Tickets.objects.filter(flight_id_id = flight_id).all()
                logger.info(f"In delete airline pk = {pk}, flight with id = {flight_id}, has related tickets, {related_tickets = }.")
                for ticket in related_tickets:
                    ticket.delete()
                flight.delete()
                info_msg = f"In delete airline pk = {pk}, flight with id = {flight_id}, and all its related tickets have been successfully deleted."
                logger.info(info_msg)
        info_msg = f"Airline company with id = {pk}, has flights, and it got successfully deleted together with all of its flights."
        airline.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CountryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Countries to be viewed.
    """
    queryset = Countries.objects.all().order_by('name')
    serializer_class = CountrySerializer
    # permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get']


class AirlineViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Airline_Companies to be viewed or edited.
    """
    queryset = Airline_Companies.objects.all().order_by('id')
    serializer_class = AirlineSerializer
    http_method_names = ['get']


class FlightViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Flights to be viewed or edited.
    """
    queryset = Flights.objects.all().order_by('id')
    serializer_class = FlightSerializer
    http_method_names = ['get']


@method_decorator(allowed_roles(['Customer']), name='dispatch')
class TicketViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Tickets to be added and viewed by the customer who owns them.
    """
    queryset = Tickets.objects.all().order_by('id')
    serializer_class = Ticket4CustomerSerializer
    http_method_names = ["get", "post", "delete"]

    def list(self, request):
        user_id = get_user_id_from_session(request=request)
        if (type(user_id)!=int):
            err_msg = f"Error! Failed to get 'user_id' from session and so couldn't fetch the correct tickets."
            logger.error(err_msg)
            return Response(err_msg, status=status.HTTP_403_FORBIDDEN)
    
        customer = Customers.objects.get(user_id=user_id)
        customer_id = customer.id
        tickets = get_tickets_by_customer(customer_id=customer_id)
        if (type(tickets)==str):
            logger.error(tickets)
            return Response(tickets, status=status.HTTP_204_NO_CONTENT)
        many = {}
        cnt = 0
        logger.info(f"got {tickets = }")
        if (type(tickets)!=Tickets):
            for t in tickets:
                cnt += 1
                many[cnt] = model_to_dict(t)
            return Response(many, status=status.HTTP_200_OK)
        tickets = model_to_dict(tickets)
        return Response(tickets, status=status.HTTP_200_OK)
       
    def retrieve(self, request, pk):
        user_id = get_user_id_from_session(request=request)
        if (type(user_id)!=int):
            err_msg = f"Error! Failed to get 'user_id' from session and so couldn't check if you have a permission to view this page. Requested pk = {pk}."
            logger.error(err_msg)
            return Response(err_msg, status=status.HTTP_403_FORBIDDEN)
    
        customer = Customers.objects.get(user_id=user_id)
        customer_id = customer.id
        requested_ticket = Tickets.objects.filter(id=pk).exists()
        if requested_ticket:
            requested_ticket = Tickets.objects.filter(id=pk)
        else:
            err_msg = f"A ticket with {pk = } doesn't exist."
            logger.error(err_msg)
            return Response(err_msg, status=status.HTTP_404_NOT_FOUND)
        ticket = {}
        if (type(requested_ticket)!=Tickets): # Always returns QuerySet.
            for t in requested_ticket:
                ticket['Your ticket'] = model_to_dict(t)
        logger.info(f"{ticket = }")
        ticket_owner_id = ticket['Your ticket']['customer_id']
        if (ticket_owner_id != customer_id):
            err_msg = f"Sorry, but you are forbidden from viewing tickets that don't belong to you."
            logger.error(err_msg)
            return Response(err_msg, status=status.HTTP_403_FORBIDDEN)
        
        return Response(ticket, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        user_id = get_user_id_from_session(request=request)
        if (type(user_id)!=int):
            err_msg = f"Error! Failed to get 'user_id' from session and so couldn't check if you have a permission to view this page."
            logger.error(err_msg)
            return Response(err_msg, status=status.HTTP_403_FORBIDDEN)
    
        customer = Customers.objects.get(user_id=user_id)
        customer_id = customer.id
        additional = {'customer_id':customer_id}

        data = dict(request.data)
        tmp = ''
        for k, v in data.items():
            if (data[k] == ['']):
                data[k] = None
            else:
                tmp = str(data[k][0])
                # print(f"{tmp = }")
                data[k] = tmp
                if tmp.isnumeric():
                    data[k] = int(tmp)
            
        # print(f"thisssss {data = }")
        serializer = Ticket4CustomerSerializer(data=data, context=additional)
        if serializer.is_valid():
            flight_id = data['flight_id_id']
            flight = Flights.objects.get(id=flight_id)
            update_tickets = flight.remaining_tickets - 1
            flight.remaining_tickets = update_tickets
            flight.save()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)
        
    def destroy(self, request, *args, **kwargs):
        try:
            pk = int(kwargs['pk'])
        except Exception as e:
            err_msg = f"{pk = } is invalid. It should be a proper ticket id which is a positive integer."
            logger.error(err_msg)
            return Response(err_msg, status=status.HTTP_400_BAD_REQUEST)

        requested_ticket = Tickets.objects.filter(id=pk).exists()
        if not requested_ticket:
            err_msg = f"A ticket with {pk = } doesn't exist."
            logger.error(err_msg)
            return Response(err_msg, status=status.HTTP_404_NOT_FOUND)
        requested_ticket = Tickets.objects.get(id=pk)
        flight_ID = requested_ticket.flight_id.id

        flight = Flights.objects.filter(id=flight_ID).exists()
        if flight:
            flight = Flights.objects.get(id=flight_ID)
            flight.remaining_tickets += 1
            flight.save()
            info_msg = f"A ticket with {pk = }, and flight with id = {flight_ID} exist. The ticket was successfully returned and deleted from the customer's ticket history."
            logger.info(info_msg)
        else: # won't happen though because when a flight gets deleted all its related tickets get deleted too
            info_msg = f"A ticket with {pk = } exists, and flight with id = {flight_ID} doesn't exist (since it was deleted from the site by its airline). The ticket was successfully deleted from the customer's ticket history."
            logger.info(info_msg)
      
        return super().destroy(request, *args, **kwargs)


@method_decorator(allowed_roles(['Customer']), name='dispatch')
class MyOwnCustomerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Customers to be viewed or edited.
    """
    queryset = Customers.objects.all().order_by('id')
    serializer_class = MyOwnCustomerSerializer
    http_method_names = ["get", "put", "patch"]

    def list(self, request):
        user_id = get_user_id_from_session(request=request)
        if (type(user_id)!=int):
            err_msg = f"Error! Failed to get 'user_id' from session and so couldn't check if you have a permission to view this page."
            logger.error(err_msg)
            return Response(err_msg, status=status.HTTP_403_FORBIDDEN)
    
        customer = Customers.objects.get(user_id=user_id)
        customer_id = customer.id
        customer = model_to_dict(customer)
        return Response({'customer':customer, 'tip':f"Use your 'customer_id' = {customer_id} (not 'user_id' = {user_id}), to edit your customer account's details."}, status=status.HTTP_200_OK)
       
    
    def retrieve(self, request, pk):
        user_id = get_user_id_from_session(request=request)
        if (type(user_id)!=int):
            err_msg = f"Error! Failed to get 'user_id' from session and so couldn't check if you have a permission to view this page."
            logger.error(err_msg)
            return Response(err_msg, status=status.HTTP_403_FORBIDDEN)
    
        customer = Customers.objects.get(user_id=user_id)
        customer_id = customer.id
        customer = model_to_dict(customer)
        return Response({'customer':customer, 'tip':f"Use your 'customer_id' = {customer_id} (not 'user_id' = {user_id}), to edit your customer account's details."}, status=status.HTTP_200_OK)
       

    def update(self, request, *args, **kwargs):
        data = dict(request.data)
        tmp = ''
        for k, v in data.items():
            if (data[k] == ['']):
                data[k] = None
            else:
                tmp = str(data[k][0])
                # print(f"{tmp = }")
                data[k] = tmp
                if tmp.isnumeric():
                    data[k] = int(tmp)
        # data.update(kwargs)
        additional = dict(kwargs)
        pk = int(kwargs['pk'])
        # logger.info(f"sending this : {data = }")
        serializer = MyOwnCustomerSerializer(data=data, context=additional)
        # print(f"{pk = }")
        user_id = get_user_id_from_session(request=request)
        if (type(user_id)!=int):
            err_msg = f"Error! Failed to get 'user_id' from session and so couldn't check if you have a permission to view this page. Requested pk = {pk}."
            logger.error(err_msg)
            return Response(err_msg, status=status.HTTP_403_FORBIDDEN)
    
        you = Customers.objects.get(user_id=user_id)
        your_customer_id = you.id
        
        if (your_customer_id != pk):
            err_msg = f"Sorry, but you are forbidden from editing customer accounts other than your own. Your customer account id = {your_customer_id}. Requested customer account id = {pk}. These ids should match."
            return Response(err_msg, status=status.HTTP_403_FORBIDDEN)
    
        if serializer.is_valid():
            updated = serializer.data
            for key, value in updated.items():
                if (hasattr(you, key)):
                    setattr(you, key, value)
            you.save()
            updated_you = Customers.objects.get(id=pk)
            updated_you = model_to_dict(updated_you)
            logger.info(updated_you)
            return Response(updated_you, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)


@method_decorator(allowed_roles(['Airline Company']), name='dispatch')
class MyOwnAirlineViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows airline companies to edit their own details.
    """
    queryset = Airline_Companies.objects.all().order_by('id')
    serializer_class = MyOwnAirlineSerializer
    http_method_names = ["get", "put", "patch"]

    def list(self, request):
        user_id = get_user_id_from_session(request=request)
        if (type(user_id)!=int):
            err_msg = f"Error! Failed to get 'user_id' from session and so couldn't check if you have a permission to view this page."
            logger.error(err_msg)
            return Response(err_msg, status=status.HTTP_403_FORBIDDEN)
    
        airline = Airline_Companies.objects.get(user_id=user_id)
        airline_id = airline.id
        airline = model_to_dict(airline)
        return Response({'airline':airline, 'tip':f"Use your 'airline_id' = {airline_id} (not 'user_id' = {user_id}), to update your airline company's details."}, status=status.HTTP_200_OK)
       
    def retrieve(self, request, pk):
        user_id = get_user_id_from_session(request=request)
        if (type(user_id)!=int):
            err_msg = f"Error! Failed to get 'user_id' from session and so couldn't check if you have a permission to view this page. Requested pk = {pk}."
            logger.error(err_msg)
            return Response(err_msg, status=status.HTTP_403_FORBIDDEN)
    
        airline = Airline_Companies.objects.get(user_id=user_id)
        airline_id = airline.id
        airline = model_to_dict(airline)
        return Response({'airline':airline, 'tip':f"Use your 'airline_id' = {airline_id} (not 'user_id' = {user_id}), to update your airline company's details."}, status=status.HTTP_200_OK)
       

    def update(self, request, *args, **kwargs):
        data = dict(request.data)
        tmp = ''
        for k, v in data.items():
            if (data[k] == ['']):
                data[k] = None
            else:
                tmp = str(data[k][0])
                # print(f"{tmp = }")
                data[k] = tmp
                if tmp.isnumeric():
                    data[k] = int(tmp)
        # data.update(kwargs)
        additional = dict(kwargs)
        pk = int(kwargs['pk'])
        logger.info(f"sending this : {data = }. additional : {additional}")
        serializer = MyOwnAirlineSerializer(data=data, context=additional)
        print(f"{pk = }")
        user_id = get_user_id_from_session(request=request)
        if (type(user_id)!=int):
            err_msg = f"Error! Failed to get 'user_id' from session and so couldn't check if you have a permission to view this page. Requested pk = {pk}."
            logger.error(err_msg)
            return Response(err_msg, status=status.HTTP_403_FORBIDDEN)
    
        you = Airline_Companies.objects.get(user_id=user_id)
        your_airline_id = you.id
        
        if (your_airline_id != pk):
            err_msg = f"Sorry, but you are forbidden from editing airline companies other than your own. Your airline company id = {your_airline_id}. Requested airline company id = {pk}. These ids should match."
            return Response(err_msg, status=status.HTTP_403_FORBIDDEN)
    
        if serializer.is_valid():
            updated = serializer.data
            for key, value in updated.items():
                if (hasattr(you, key)):
                    setattr(you, key, value)
            logger.info(f"Your airline : {you =  }")
            you.save()
            updated_you = Airline_Companies.objects.get(id=pk)
            updated_you = model_to_dict(updated_you)
            logger.info(updated_you)
            return Response(updated_you, status=status.HTTP_200_OK)
        else:
            logger.info("whyyyyyyyyyyyyyyyyyyyyyyy")
            return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)


@method_decorator(allowed_roles(['Airline Company']), name='dispatch')
class MyOwnFlightViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Flights to be viewed or edited.
    """
    queryset = Flights.objects.all().order_by('id')
    serializer_class = Flight4AirlineSerializer
    http_method_names = ["get", "put", "patch"]

    def list(self, request):
        user_id = get_user_id_from_session(request=request)
        if (type(user_id)!=int):
            err_msg = f"Error! Failed to get 'user_id' from session and so couldn't fetch the correct flights."
            logger.error(err_msg)
            return Response(err_msg, status=status.HTTP_403_FORBIDDEN)
    
        airline = Airline_Companies.objects.get(user_id=user_id)
        airliner_id = airline.id
        flights = get_flights_by_airlineID(airline_id=airliner_id)
        if (type(flights)==str):
            logger.error(flights)
            return Response(flights, status=status.HTTP_204_NO_CONTENT)
        many = {}
        cnt = 0
        logger.info(f"got {flights = }")
        if (type(flights)!=Flights):
            for f in flights:
                cnt += 1
                many[cnt] = model_to_dict(f)
            return Response(many, status=status.HTTP_200_OK)
        flights = model_to_dict(flights)
        return Response(flights, status=status.HTTP_200_OK)
       
    def retrieve(self, request, pk):
        user_id = get_user_id_from_session(request=request)
        if (type(user_id)!=int):
            err_msg = f"Error! Failed to get 'user_id' from session and so couldn't check if you have a permission to view this page. Requested pk = {pk}."
            logger.error(err_msg)
            return Response(err_msg, status=status.HTTP_403_FORBIDDEN)
    
        airline = Airline_Companies.objects.get(user_id=user_id)
        airline_id = airline.id
        requested_flight = Flights.objects.filter(id=pk).exists()
        if requested_flight:
            requested_flight = Flights.objects.filter(id=pk)
        else:
            err_msg = f"A flight with {pk = } doesn't exist."
            logger.error(err_msg)
            return Response(err_msg, status=status.HTTP_404_NOT_FOUND)
        flight = {}
        if (type(requested_flight)!=Tickets): # Always returns QuerySet.
            for t in requested_flight:
                flight['Your flight'] = model_to_dict(t)
        logger.info(f"{flight = }")
        flight_owner_id = flight['Your flight']['airline_company_id']
        if (flight_owner_id != airline_id):
            err_msg = f"Sorry, but you are forbidden from viewing flights that don't belong to you."
            logger.error(err_msg)
            return Response(err_msg, status=status.HTTP_403_FORBIDDEN)
        
        return Response(flight, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        data = dict(request.data)
        tmp = ''
        for k, v in data.items():
            if (data[k] == ['']):
                data[k] = None
            else:
                tmp = str(data[k][0])
                # print(f"{tmp = }")
                data[k] = tmp
                if tmp.isnumeric():
                    data[k] = int(tmp)
        # data.update(kwargs)
        additional = dict(kwargs)
        pk = int(kwargs['pk'])
        # logger.info(f"sending this : {data = }")
        serializer = Flight4AirlineSerializer(data=data, context=additional)
        # print(f"{pk = }")
        user_id = get_user_id_from_session(request=request)
        if (type(user_id)!=int):
            err_msg = f"Error! Failed to get 'user_id' from session and so couldn't check if you have a permission to view this page. Requested pk = {pk}."
            logger.error(err_msg)
            return Response(err_msg, status=status.HTTP_403_FORBIDDEN)
    
        requested_flight = Flights.objects.filter(id=pk).exists()
        if requested_flight:
            requested_flight = Flights.objects.filter(id=pk)
        else:
            err_msg = f"A flight with {pk = } doesn't exist."
            logger.error(err_msg)
            return Response(err_msg, status=status.HTTP_404_NOT_FOUND)
        
        flight = {}
        if (type(requested_flight)!=Flights): # Always returns QuerySet.
            for f in requested_flight:
                flight['Your flight'] = model_to_dict(f)
        logger.info(f"{flight = }")
        flight_owner_id = flight['Your flight']['airline_company_id']
        
        you = Airline_Companies.objects.get(user_id=user_id)
        your_airline_id = you.id
        
        if (flight_owner_id != your_airline_id):
            err_msg = f"Sorry, but you are forbidden from editing the flights which don't belong to your own airline company. Your airline company id is: {your_airline_id}. The requested flight belongs to an airline company whose id is: {flight_owner_id}. These ids should match."
            return Response(err_msg, status=status.HTTP_403_FORBIDDEN)
    
        flight = Flights.objects.get(id=pk)
        if serializer.is_valid():
            updated = serializer.data
            for key, value in updated.items():
                if (hasattr(flight, key)):
                    setattr(flight, key, value)
            flight.save()
            updated_you = Flights.objects.get(id=pk)
            updated_you = model_to_dict(updated_you)
            logger.info(updated_you)
            return Response(updated_you, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)


@method_decorator(allowed_roles(['Airline Company']), name='dispatch')
class AddMyOwnFlightViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Flights to be added.
    """
    queryset = Flights.objects.all().order_by('id')
    serializer_class = AddFlight4AirlineSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        user_id = get_user_id_from_session(request=request)
        if (type(user_id)!=int):
            err_msg = f"Error! Failed to get 'user_id' from session and so couldn't check if you have a permission to view this page."
            logger.error(err_msg)
            return Response(err_msg, status=status.HTTP_403_FORBIDDEN)
    
        airline = Airline_Companies.objects.get(user_id=user_id)
        airline_id = airline.id
        additional = {'airline_id':airline_id}

        data = dict(request.data)
        tmp = ''
        for k, v in data.items():
            if (data[k] == ['']):
                data[k] = None
            else:
                tmp = str(data[k][0])
                print(f"{tmp = }")
                data[k] = tmp
                if tmp.isnumeric():
                    data[k] = int(tmp)
            
        # print(f"thisssss {data = }")
        serializer = AddFlight4AirlineSerializer(data=data, context=additional)
        if serializer.is_valid():
            serializer.save()
            flight_id = Flights.objects.latest('id').id
            return Response({f'Flight id = {flight_id}': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)


@method_decorator(allowed_roles(['Airline Company']), name='dispatch')
class DeleteMyOwnFlightViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Flights to be deleted.
    """
    queryset = Flights.objects.all().order_by('id')
    serializer_class = FlightSerializer
    http_method_names = ['delete']

    
    def destroy(self, request, *args, **kwargs):
        pk = int(kwargs['pk'])
        user_id = get_user_id_from_session(request=request)
        if (type(user_id)!=int):
            err_msg = f"Error! Failed to get 'user_id' from session and so couldn't check if you have a permission to view this page."
            logger.error(err_msg)
            return Response(err_msg, status=status.HTTP_403_FORBIDDEN)
    
        requested_flight = Flights.objects.filter(id=pk).exists()
        if not requested_flight:
            err_msg = f"Bad input. Your requested flight id = {pk} doesn't exist."
            logger.error(err_msg)
            return Response(err_msg, status=status.HTTP_404_NOT_FOUND)
        
        requested_flight = Flights.objects.get(id=pk)
        req_flight_airline_id = requested_flight.airline_company_id.id

        airline = Airline_Companies.objects.get(user_id=user_id)
        airline_id = airline.id

        if (airline_id != req_flight_airline_id):
            err_msg = f"Sorry, but you are forbidden from deleting flights other than your own. Your airline company id = {airline_id}, but your requested flight pk = {pk}, belongs to an airline company with id = {req_flight_airline_id}. Make sure that you own the flights which you request to delete."
            logger.error(err_msg)
            return Response(err_msg, status=status.HTTP_403_FORBIDDEN)
        
        related_tickets = Tickets.objects.filter(flight_id_id = pk).exists()
        if not related_tickets:
            requested_flight.delete()
            info_msg = f"Your requested flight with id = {pk} has been successfully deleted."
            logger.info(info_msg)
            return Response(status=status.HTTP_204_NO_CONTENT)

        related_tickets = Tickets.objects.filter(flight_id_id = pk).all()
        logger.info(f"In delete flight pk = {pk}, related tickets were found, {related_tickets = }.")
        for ticket in related_tickets:
            ticket.delete()

        requested_flight.delete()
        info_msg = f"Your requested flight with id = {pk}, and all its related tickets have been successfully deleted."
        logger.info(info_msg)
        return Response(status=status.HTTP_204_NO_CONTENT)


class TicketExistsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows you to check if a ticket to a flight with a certain id exists.
    """
    queryset = Tickets.objects.all().order_by('id')
    serializer_class = Ticket4CustomerSerializer
    http_method_names = ["get"]

    def list(self, request):
        err_msg = "List isn't available here. This API is meant to be used only via inputting a certain flight id in the retrieve path, to check if a ticket to that flight exists."
        return Response(err_msg, status=status.HTTP_403_FORBIDDEN)


    def retrieve(self, request, pk):
        try:
            flight_id = int(pk)
            if not (Flights.objects.filter(id=flight_id).exists()):
                err_msg = f"BAD INPUT! A flight with id {flight_id} doesn't exist."
                logger.error(err_msg)
                return Response(err_msg, status=status.HTTP_400_BAD_REQUEST)
            
            flight = Flights.objects.get(id=flight_id)
            remaining_tickets = flight.remaining_tickets
            if (remaining_tickets<1):
                err_msg = f"The tickets of the flight with id = {flight_id}, were already all sold out."
                logger.error(err_msg)
                return Response(err_msg, status=status.HTTP_410_GONE)
            info_msg = f"Good! A ticket to flight with id {flight_id} exists, and can be sold to you on the flights page if you are a registered and logged customer."
            return Response(info_msg, status=status.HTTP_200_OK)

        except Exception as e:
            err_msg = f"Failed to check if a ticket to flight with id {flight_id} exists. Error: {e}"
            logger.error(err_msg)
            return Response(err_msg, status=status.HTTP_400_BAD_REQUEST)
        

class CustomerExistsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows you to check if a Customers instance with a certain user id exists.
    """
    queryset = Customers.objects.all().order_by('id')
    serializer_class = CustomerSerializer
    http_method_names = ["get"]

    def list(self, request):
        err_msg = "List isn't available here. This API is meant to be used only via inputting a certain user id in the retrieve path, to check if a customer instance with that user id exists."
        return Response(err_msg, status=status.HTTP_403_FORBIDDEN)


    def retrieve(self, request, pk):
        try:
            user_id = int(pk)
            if not (Users.objects.filter(id=user_id).exists()):
                err_msg = f"BAD INPUT! A user with id {user_id} doesn't exist."
                logger.error(err_msg)
                return Response(err_msg, status=status.HTTP_400_BAD_REQUEST)
            
            if not (Customers.objects.filter(user_id_id=user_id).exists()):
                err_msg = f"A customer with user id: {user_id} doesn't exist."
                logger.error(err_msg)
                return Response(err_msg, status=status.HTTP_404_NOT_FOUND)
            
            info_msg = f"A customer with user id: {user_id} exists."
            return Response(info_msg, status=status.HTTP_200_OK)
        
        except Exception as e:
            err_msg = f"Failed to check if a customer with user id {user_id} exists. Error: {e}"
            logger.error(err_msg)
            return Response(err_msg, status=status.HTTP_400_BAD_REQUEST)
        

# regular views (facade functions): =============================================================================================================================

@extend_schema(
    request=SignupSerializer,
    responses={201: dict, 404: str, 400: dict})
@api_view(['POST'])
@allowed_roles(['Anonymous'])
def signup_api(request):

    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        username = request.data['username']
        password = request.data['password']
        role_or_false, token_or_err = Anonymous_Facade.login_user(request=request, username=username, password=password)

        if role_or_false==False:
            return Response(token_or_err, status=status.HTTP_404_NOT_FOUND)

        user = Users.objects.get(username=username)
        user_id = user.id
        serializer = UserSerializer(user)
        response = Response({'token': token_or_err,'user_id': user_id, 'msg': f"Welcome, {username}. You are logged in now. Your user role is: {role_or_false}.", 'user': serializer.data}, status=status.HTTP_201_CREATED)
        
        response.set_cookie('user_token', token_or_err, samesite='None', secure=True)

        return response
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=LoginSerializer,
    responses={200: dict, 404: str})
@api_view(['POST'])
@allowed_roles(['Anonymous'])
def login_user_api(request):

    username = request.data['username']
    password = request.data['password']
    role_or_false, token_or_err = Anonymous_Facade.login_user(request=request, username=username, password=password)

    if role_or_false==False:
        return Response(token_or_err, status=status.HTTP_404_NOT_FOUND)

    user = Users.objects.get(username=username)
    user_id = user.id
    serializer = UserSerializer(user)
    response = Response({'token': token_or_err, 'user_id': user_id, 'msg': f"Welcome back, {username}. You are logged in now. Your user role is: {role_or_false}.", 'user': serializer.data}, status=status.HTTP_200_OK)

    response.set_cookie('user_token', token_or_err, samesite='None', secure=True)

    return response

@extend_schema(responses={200: str})
@api_view(['POST'])
def logout_user_api(request):

    msg = Anonymous_Facade.logout_user(request=request)
    response = Response(msg, status=status.HTTP_200_OK)

    response.delete_cookie('user_token')

    return response


@extend_schema(
        request=FlightParametersSerializer,
        responses={200: dict, 404: str, 400: dict})
@api_view(['POST'])
def get_flights_by_parameters_D(request):

    serializer = FlightParametersSerializer(data=request.data)
    if serializer.is_valid():
        filters = dict(serializer.data)

        failed, flights = Facade_Base.get_flights_by_parameters_Dynamic(filters=filters)
        
        if failed==False:
            cnt = 0
            flights = list(flights)
            print(f"{flights = }")
            filtered_flights = {}
            if (type(flights)!=Flights): # Always returns QuerySet.
                for flight in flights:
                    cnt += 1
                    filtered_flights[cnt] = model_to_dict(flight)
            print(f"{filtered_flights = }")
            if (filtered_flights == {}):
                return Response("No flights with the parameters that you've requested exist.", status=status.HTTP_404_NOT_FOUND)
            return Response(filtered_flights, status=status.HTTP_200_OK)
            
        return Response(flights, status=status.HTTP_404_NOT_FOUND)

    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
        request=AirlineParametersSerializer,
        responses={200: dict, 404: str, 400: dict})
@api_view(['POST'])
def get_airlines_by_parameters_D(request):

    serializer = AirlineParametersSerializer(data=request.data)
    if serializer.is_valid():
        filters = dict(serializer.data)

        failed, airlines = Facade_Base.get_airlines_by_parameters_Dynamic(filters=filters)
        
        if failed==False:
            cnt = 0
            airlines = list(airlines)
            print(f"{airlines = }")
            filtered_airlines = {}
            if (type(airlines)!=Airline_Companies): # Always returns QuerySet.
                for airline in airlines:
                    cnt += 1
                    filtered_airlines[cnt] = model_to_dict(airline)
            print(f"{filtered_airlines = }")
            if (filtered_airlines == {}):
                return Response("No airlines with the parameters that you've requested exist.", status=status.HTTP_404_NOT_FOUND)
            return Response(filtered_airlines, status=status.HTTP_200_OK)
            
        return Response(airlines, status=status.HTTP_404_NOT_FOUND)

    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
        request=UsernameSerializer,
        responses={200: dict, 400: dict})
@api_view(['POST'])
@allowed_roles(['Administrator'])
def get_userId_by_username(request):

    data = dict(request.data)
    username = data['username']
    if (type(username) == list):
        username = username[0]

    user_id = Administrator_Facade.get_userID_by_username(username=username)

    if (user_id == 0):
        err_msg = f"A user with {username = } doesn't exists."
        logger.error(err_msg)
        return Response({'Error': err_msg}, status=status.HTTP_400_BAD_REQUEST)

    info_msg = f"A user with {username = } exists, and their id is: {user_id}."
    logger.info(info_msg)
    return Response({'id': user_id}, status=status.HTTP_200_OK)


@extend_schema(
        request=NameSerializer,
        responses={200: dict, 400:dict, 404: dict})
@api_view(['POST'])
def get_instances_by_name(request):
    """
        To search for existing instances by name, in the "model" field you must input one of the following options: "user" / "customer" / "admin" / "airline" / "country".
    """

    str2models = {"user":Users, "customer":Customers, "admin":Administrators, "airline":Airline_Companies , "country":Countries}
    data = dict(request.data)
    keys = str2models.keys()
    model = data['model']
    if (type(model) == list):
        model = model[0]
    if model not in keys:
        err_msg = f"Bad input. Your {model = } must be one of these options: {list(keys)}."
        logger.error(err_msg)
        return Response({'Error': err_msg}, status=status.HTTP_400_BAD_REQUEST)

    model = str2models[model]
    name = data['name']
    if (type(name) == list):
        name = name[0]
    instances = Facade_Base.get_instances_by_name(some_model=model, name=name)

    if instances is False:
        info_msg = f"Instances of {model} with {name = } don't exist."
        logger.info(info_msg)
        return Response({'Info': info_msg}, status=status.HTTP_404_NOT_FOUND)

    cnt = 0
    instances = list(instances)
    print(f"{instances = }")
    instances_dict = {}
    if (type(instances) not in str2models.values()): # Always returns QuerySet.
        for instance in instances:
            cnt += 1
            instances_dict[cnt] = model_to_dict(instance)
    info_msg = f"Instances of {model} with {name = } do exist. Here they are: {instances_dict}."
    logger.info(info_msg)
    return Response({'found': instances_dict}, status=status.HTTP_200_OK)


@extend_schema()
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
def test_token(request):
    return Response("passed!")



