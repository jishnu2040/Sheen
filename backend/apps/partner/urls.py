from django.urls import path
from .views import ServiceTypeListView, PartnerCreateView, PartnerListView, PartnerServiceListView, AddServiceToPartnerView

urlpatterns = [
    path('service-types/', ServiceTypeListView.as_view(), name='service-type-list'),
    path('create-partner/', PartnerCreateView.as_view(), name='partner-creation'),
    path('list-partner/', PartnerListView.as_view(), name='partner-list-view'),
    path('<int:user_id>/services/', PartnerServiceListView.as_view(), name='partner-service-list'),
    path('<int:user_id>/services/add/', AddServiceToPartnerView.as_view(), name='add-service-to-partner')
]
