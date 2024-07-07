from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import UserManager
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

# Create your models here.

AUTH_PROVIDER ={
    'email': 'email',
    'google':'google',
    'github':'hithub',
    'facebook':'facebook'
}



class User(AbstractBaseUser, PermissionsMixin):

    USER_TYPE_CHOICES = (
        ('customer', 'Customer'),
        ('partner', 'Business Partner'),
    )
    
    email = models.EmailField(max_length=255, unique=True, verbose_name=_("Email address"))
    first_name =models.CharField(max_length=100, verbose_name=_("First Name"))
    last_name =models.CharField(max_length=100, verbose_name=_("Last Name"))
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    auth_provider=models.CharField(max_length=100, default=AUTH_PROVIDER.get('email'))
    user_type = models.CharField(max_length=50, choices=USER_TYPE_CHOICES, default='customer')


    


    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["first_name", "last_name"]


    #here i'm separate business logic layer from data layer
    
    objects = UserManager()

    def __str__(self):
        return self.email
    

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


    def token(self):
        refresh_token=RefreshToken.for_user(self)
        return{
            'refresh':str(refresh_token),
            'access':str(refresh_token.access_token)
        }

class OneTimePassword(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    code=models.CharField(max_length=6, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"{self.user.first_name}-passcode"
    
    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=15)  # Set expiration to 15 minutes from creation
        super().save(*args, **kwargs)
    


class Partner(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='partner_profile')
    company_name = models.CharField(max_length=255, verbose_name=_("Company Name"))
    address = models.CharField(max_length=255, verbose_name=_("Address"))
    phone = models.CharField(max_length=20, verbose_name=_("Phone Number"))
    website = models.CharField(max_length=200, blank=True, null=True, verbose_name=_("Website"))
    latitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name=_("Latitude"))
    longitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name=_("Longitude"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name
    
class BusinessType(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name=_("Business Type"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Service(models.Model):
    partner = models.ForeignKey('Partner', related_name='services', on_delete=models.CASCADE)
    business_type = models.ForeignKey('BusinessType', related_name='services', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name=_("Service Name"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Price"))
    duration = models.DurationField(verbose_name=_("Duration"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

