from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ServiceTypeListView, PartnerCreateView

# router = DefaultRouter()
# router.register(r'partner_details', PartnerDetailViewSet)

urlpatterns = [
    path('service-types/', ServiceTypeListView.as_view(), name='service-type-list'),
    path('create-partner/', PartnerCreateView.as_view(), name='partner-creation')
]
