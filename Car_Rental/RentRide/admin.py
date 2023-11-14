from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class CarDealerAdmin(admin.ModelAdmin):
     def delete_model(self, request, obj):
         obj.user.delete()
         obj.delete()

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(CarDealer, CarDealerAdmin)
admin.site.register(Location)
admin.site.register(Car)
admin.site.register(Customer)
admin.site.register(Order)