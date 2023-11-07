from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("customer_login/", views.customer_login, name="customer_login"),
]
