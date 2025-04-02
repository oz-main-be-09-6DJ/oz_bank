from django.urls import path
from . import views

urlpatterns = [
    path('test-home/', views.test_home, name='test-home'),
]