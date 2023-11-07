from django.contrib import admin
from .models import Location, CarDealer, Car, Customer, Order

admin.site.register(Location)
admin.site.register(CarDealer)
admin.site.register(Car)
admin.site.register(Customer)
admin.site.register(Order)