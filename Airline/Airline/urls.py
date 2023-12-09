from django.urls import path, include
from airline_reservation_system import api
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

# ===================================================================================
all = DefaultRouter()
user = DefaultRouter()
admin = DefaultRouter()
airline = DefaultRouter()
customer = DefaultRouter()

# ===================================================================================
all.register(r"country-for-all", api.CountryViewSet)
all.register(r"airline-for-all", api.AirlineViewSet)
all.register(r"flight-for-all", api.ShowFlightViewSet)
all.register(r"does-flight-has-tickets", api.TicketExistsViewSet)

# ===================================================================================
user.register(r"my-own-user", api.MyOwnUserViewSet)

# ===================================================================================
admin.register(r"role-for-admins", api.Role4AdminViewSet)
admin.register(r"user-for-admins", api.User4AdminViewSet)
admin.register(r"customer-for-admins", api.Customer4AdminViewSet)
admin.register(r"airline-for-admins", api.Airline4AdminViewSet)
admin.register(r"admin-for-admins", api.Admin4AdminViewSet)
admin.register(r"my-own-admin-delete", api.DeleteAdminViewSet)

# ===================================================================================
airline.register(r"my-own-airline", api.MyOwnAirlineViewSet)
airline.register(r"my-own-flight", api.MyOwnFlightViewSet)
airline.register(r"my-own-flight-add", api.AddMyOwnFlightViewSet)
airline.register(r"my-own-flight-delete", api.DeleteMyOwnFlightViewSet)

# ===================================================================================
customer.register(r"ticket-for-customers", api.TicketViewSet)
customer.register(r"my-own-customer", api.MyOwnCustomerViewSet)
customer.register(r"become-a-customer", api.Customer4CustomerUserAdd)
customer.register(r"does-customer-exists", api.CustomerExistsViewSet)

# ===================================================================================
urlpatterns = [

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/', SpectacularSwaggerView.as_view(url_name='schema')),

    path('all/models/', include(all.urls)),
    path('user/models/', include(user.urls)),
    path('admin/models/', include(admin.urls)),
    path('airline/models/', include(airline.urls)),
    path('customer/models/', include(customer.urls)),

    path('all/signup/', api.signup_api, name="signup_api"),
    path('all/login/', api.login_user_api, name="login_api"),
    path('all/search_by_name/', api.get_instances_by_name, name="name_search"),
    path('all/get_flights_by_parameters/', api.get_flights_by_parameters_DA, name="get_flights_by_parameters"),
    path('all/get_airlines_by_parameters/', api.get_airlines_by_parameters_D, name="get_airlines_by_parameters"),
    path('user/logout/', api.logout_user_api, name="logout_api"),
    path('admin/get-user-id-for-admins/', api.get_userId_by_username, name="user-id"),

] 