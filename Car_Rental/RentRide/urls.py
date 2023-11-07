from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("customer_login/", views.customer_login, name="customer_login"),
    path("customer_signup/", views.customer_signup, name="customer_signup"),
    path('logout/', views.logout_view, name='logout'),
]
