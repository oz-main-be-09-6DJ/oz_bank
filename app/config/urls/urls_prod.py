from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/',include('users.urls')),
    path('api/accounts/',include('account.urls')),
    path('api/transaction/',include('transaction.urls')),
    path('api/analysis/',include('analysis.urls')),
]