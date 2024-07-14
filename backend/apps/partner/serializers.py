from rest_framework import serializers
from .models import ServiceType, PartnerDetail


class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = ['id', 'name']



class PartnerCreateSerializer(serializers.ModelSerializer):
    service_type = serializers.PrimaryKeyRelatedField(queryset=ServiceType.objects.all(), many=True)

    class Meta:
        model = PartnerDetail
        fields = ['user', 'business_name', 'website', 'service_type', 'team_size', 'location']

    def create(self, validated_data):
        service_types = validated_data.pop('service_type')
        partner_detail = PartnerDetail.objects.create(**validated_data)
        partner_detail.service_type.set(service_types)
        return partner_detail