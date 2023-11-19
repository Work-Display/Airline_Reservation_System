from django.urls import path, include
from airline_reservation_system import api
from django.contrib.staticfiles.storage import staticfiles_storage
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r"role-for-admins", api.Role4AdminViewSet)
router.register(r"user-for-admins", api.User4AdminViewSet)
router.register(r"customer-for-admins", api.Customer4AdminViewSet)
router.register(r"airline-for-admins", api.Airline4AdminViewSet)
router.register(r"admin-for-admins", api.Admin4AdminViewSet)
router.register(r"my-own-admin-delete", api.DeleteAdminViewSet)
router.register(r"country-for-all", api.CountryViewSet)
router.register(r"airline-for-all", api.AirlineViewSet)
router.register(r"flight-for-all", api.FlightViewSet)
router.register(r"ticket-for-customers", api.TicketViewSet)
router.register(r"does-flight-has-tickets", api.TicketExistsViewSet)
router.register(r"my-own-customer", api.MyOwnCustomerViewSet)
router.register(r"become-a-customer", api.Customer4CustomerUserAdd)
router.register(r"does-customer-exists", api.CustomerExistsViewSet)
router.register(r"my-own-airline", api.MyOwnAirlineViewSet)
router.register(r"my-own-flight", api.MyOwnFlightViewSet)
router.register(r"my-own-flight-add", api.AddMyOwnFlightViewSet)
router.register(r"my-own-flight-delete", api.DeleteMyOwnFlightViewSet)
router.register(r"my-own-user", api.MyOwnUserViewSet)


urlpatterns = [

    path('api/models/', include(router.urls)),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/', SpectacularSwaggerView.as_view(url_name='schema')),

    path('api/signup/', api.signup_api, name="signup_api"),
    path('api/login/', api.login_user_api, name="login_api"),
    path('api/logout/', api.logout_user_api, name="logout_api"),
    path('api/get-user-id-for-admins/', api.get_userId_by_username, name="user-id"),
    path('api/get_flights_by_parameters/', api.get_flights_by_parameters_D, name="get_flights_by_parameters"),
    path('api/get_airlines_by_parameters/', api.get_airlines_by_parameters_D, name="get_airlines_by_parameters"),

] 