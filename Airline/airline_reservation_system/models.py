from django.db import models
from django.contrib.auth.models import AbstractUser
from django_resized import ResizedImageField


class User_Roles(models.Model):
    id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return self.role_name
    

class Users(AbstractUser):
  id = models.BigAutoField(primary_key=True)
  username = models.CharField(max_length = 20, unique = True)
  email = models.EmailField(unique = True)
  user_role = models.ForeignKey(User_Roles, on_delete=models.CASCADE, related_name='users') 
  thumbnail = ResizedImageField(size=[500, None], upload_to='./web-design/upload_img/user_thumbnails/', blank=True, null=True)
  REQUIRED_FIELDS = ['email', 'user_role']
  
  def __str__(self):
        return self.username
  
  def get_role(self):
        return self.user_role.role_name


class Customers(models.Model):
    id = models.BigAutoField(primary_key=True, unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    address = models.CharField(max_length=150)
    phone_no = models.CharField(max_length=20, unique=True)
    credit_card_no = models.CharField(max_length=19, unique=True)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='customers', unique=True)  


class Administrators(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='administrators', unique=True)


class Countries(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=56, unique=True)
    flag = ResizedImageField(size=[240, 180], force_format='PNG', upload_to='./web-design/upload_img/user_flags/', blank=True, null=True)


class Airline_Companies(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=30, unique=True)
    country_id = models.ForeignKey(Countries, on_delete=models.CASCADE, related_name='airlines') 
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='airlines', unique=True) 


class Flights(models.Model):
    id = models.BigAutoField(primary_key=True)                    
    airline_company_id = models.ForeignKey(Airline_Companies, on_delete=models.CASCADE, related_name='flights')  
    origin_country_id = models.ForeignKey(Countries, on_delete=models.CASCADE, related_name='flight_origin')  
    destination_country_id = models.ForeignKey(Countries, on_delete=models.CASCADE, related_name='flight_destination') 
    departure_time = models.DateTimeField()
    landing_time = models.DateTimeField()
    remaining_tickets = models.IntegerField(default=0)


class Tickets(models.Model):
    id = models.BigAutoField(primary_key=True)
    flight_id = models.ForeignKey(Flights, on_delete=models.CASCADE, related_name='tickets')  
    customer_id = models.ForeignKey(Customers, on_delete=models.CASCADE, related_name='tickets') 

    class Meta:
        unique_together = ["flight_id", "customer_id"]


class APICounter(models.Model):
    count = models.PositiveIntegerField(default=0)