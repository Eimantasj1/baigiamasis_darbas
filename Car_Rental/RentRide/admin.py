from django.contrib import admin
from .models import Car, Rental

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'year', 'price_per_day', 'is_available')
    list_filter = ('is_available',)
    search_fields = ('brand', 'model', 'year')
    prepopulated_fields = {'car_image': ('brand', 'model')}

@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ('car', 'user', 'reservation_date', 'return_date')
    list_filter = ('car', 'user')
    search_fields = ('car__brand', 'car__model', 'user__username')