from rest_framework import viewsets, generics
from rest_framework.response import Response
from .models import ServiceType, PartnerDetail
from .serializers import ServiceTypeSerializer, PartnerCreateSerializer,PartnerDetailSerializer
from rest_framework import status


class ServiceTypeListView(generics.ListAPIView):
    queryset = ServiceType.objects.all()
    serializer_class = ServiceTypeSerializer


class PartnerCreateView(generics.CreateAPIView):
    queryset = PartnerDetail.objects.all()
    serializer_class = PartnerCreateSerializer

    def create(self, request, *args, **kwargs):
        
        print("POST data:", request.data)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PartnerListView(generics.ListAPIView):
    queryset = PartnerDetail.objects.all()
    serializer_class = PartnerDetailSerializer
    
