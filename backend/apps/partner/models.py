from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class ServiceType(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, null=True) 
    created_at = models.DateTimeField(default=timezone.now)  
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return self.name


class PartnerDetail(models.Model):
    business_name = models.CharField(max_length=200)
    website = models.URLField(blank=True, null=True)
    service_type = models.ManyToManyField(ServiceType, related_name='partners')
    team_size = models.IntegerField()
    location = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    def __str__(self):
        return self.business_name
