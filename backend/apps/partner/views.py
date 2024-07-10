from rest_framework import viewsets
from .models import PartnerDetail
from .serializers import PartnerDetailSerializer

class PartnerDetailViewSet(viewsets.ModelViewSet):
    queryset = PartnerDetail.objects.all()
    serializer_class = PartnerDetailSerializer
