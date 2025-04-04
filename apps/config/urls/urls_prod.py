from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include('apps.users.urls')),
    path('api/accounts/', include('apps.account.urls')),
    path('api/transaction/', include('apps.transaction.urls')),
    path('api/analysis/', include('apps.analysis.urls')),
]