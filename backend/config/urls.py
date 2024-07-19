from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('apps.accounts.urls')),
    path('api/v1/Oauth/', include('apps.social_accounts.urls')),
    path('api/v1/partner/', include('apps.partner.urls')),
    path('api/v1/admin/', include('apps.Admin.urls'))
]

