from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PartnerDetailViewSet

router = DefaultRouter()
router.register(r'partner_details', PartnerDetailViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
