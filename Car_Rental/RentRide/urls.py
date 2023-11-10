from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("customer_login/", views.customer_login, name="customer_login"),
    path("customer_signup/", views.customer_signup, name="customer_signup"),
    path('logout/', views.logout_view, name='logout'),
    path("customer_homepage/", views.customer_homepage, name="customer_homepage"),
    path("search_results/", views.search_results, name="search_results"),
    path("car_rent/", views.car_rent, name="car_rent"),
    path("car_dealer_login/", views.car_dealer_login, name="car_dealer_login"),
    path("car_dealer_signup/", views.car_dealer_signup, name="car_dealer_signup"),
    path("all_cars/", views.all_cars, name="all_cars"),
    path("add_car/", views.add_car, name="add_car"),
    path("all_orders/", views.all_orders, name="all_orders"),
]
