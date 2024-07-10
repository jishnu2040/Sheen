from django.contrib import admin
from .models import PartnerDetail, ServiceType

@admin.register(PartnerDetail)
class PartnerDetailAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'website', 'team_size', 'location', 'updated_at')
    filter_horizontal = ('service_type',)  # To add a widget for selecting many-to-many relationships

admin.site.register(ServiceType)
