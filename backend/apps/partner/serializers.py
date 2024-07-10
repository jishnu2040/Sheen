from rest_framework import serializers
from .models import PartnerDetail, ServiceType

class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = ['id', 'name']

class PartnerDetailSerializer(serializers.ModelSerializer):
    service_type = ServiceTypeSerializer(many=True)

    class Meta:
        model = PartnerDetail
        fields = ['id', 'business_name', 'website', 'service_type', 'team_size', 'location', 'updated_at']

    def create(self, validated_data):
        service_type_data = validated_data.pop('service_type')
        partner_detail = PartnerDetail.objects.create(**validated_data)
        for service_data in service_type_data:
            service_type, created = ServiceType.objects.get_or_create(**service_data)
            partner_detail.service_type.add(service_type)
        return partner_detail

    def update(self, instance, validated_data):
        service_type_data = validated_data.pop('service_type')
        instance.business_name = validated_data.get('business_name', instance.business_name)
        instance.website = validated_data.get('website', instance.website)
        instance.team_size = validated_data.get('team_size', instance.team_size)
        instance.location = validated_data.get('location', instance.location)
        instance.save()

        instance.service_type.clear()
        for service_data in service_type_data:
            service_type, created = ServiceType.objects.get_or_create(**service_data)
            instance.service_type.add(service_type)
        
        return instance
