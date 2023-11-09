from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator 
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

class Location(models.Model):
    city = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.city

class CarDealer(models.Model):
    car_dealer = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone = models.CharField(validators=[MinLengthValidator(10), MaxLengthValidator(10)], max_length=10)
    location = models.OneToOneField(Location, on_delete=models.PROTECT)
    earnings = models.IntegerField(default=0)
    type = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return str(self.car_dealer)

def validate_car_image(value):
    allowed_formats = ('.jpg', '.jpeg', '.png')
    if not value.name.lower().endswith(allowed_formats):
        raise models.ValidationError(f"Only {', '.join(allowed_formats)} images are allowed.")

class Car(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="car_images/", validators=[validate_car_image])
    car_dealer = models.ForeignKey(CarDealer, on_delete=models.PROTECT)
    capacity = models.PositiveSmallIntegerField()
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    is_available = models.BooleanField(default=True)
    rent = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.name

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone = models.CharField(validators=[MinLengthValidator(10), MaxLengthValidator(10)], max_length=10)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return str(self.user)

class Order(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    car_dealer = models.ForeignKey(CarDealer, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    rent = models.CharField(max_length=10)
    days = models.PositiveSmallIntegerField()
    is_complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
