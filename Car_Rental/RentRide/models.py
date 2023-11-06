from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.urls import reverse
from datetime import date
from django.utils.translation import gettext_lazy as _

User = get_user_model()

def validate_car_image(value):
    if not value:
        raise ValidationError("Image is required for a car.")

class Car(models.Model):
    brand = models.CharField(max_length=50, db_index=True)
    model = models.CharField(max_length=50)
    year = models.PositiveSmallIntegerField()
    price_per_day = models.DecimalField(max_digits=8, decimal_places=2)
    car_image = models.ImageField(upload_to='car_images/', null=True, blank=True, validators=[validate_car_image])
    is_available = models.BooleanField(default=True)
    notes = models.TextField(max_length=500, null=True, blank=True)

    class Meta:
        verbose_name = _("car")
        verbose_name_plural = _("cars")

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"

    def get_absolute_url(self):
        return reverse("car_detail", kwargs={"pk": self.pk})

class Rental(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reservation_date = models.DateField()
    return_date = models.DateField()

    class Meta:
        verbose_name = _("rental")
        verbose_name_plural = _("rentals")

    def save(self, *args, **kwargs):
        today = date.today()
        if self.reservation_date < today:
            raise ValidationError(_("Reservation date cannot be earlier than today."))
        elif self.return_date <= self.reservation_date:
            raise ValidationError(_("Return date cannot be earlier than or the same as reservation date."))
        
        rental_for_car = Rental.objects.filter(car=self.car, return_date__gte=self.reservation_date, reservation_date__lte=self.return_date)
        if rental_for_car.exists():
            raise ValidationError(_("This car is already booked for the selected dates."))
        
        self.car.is_available = False
        self.car.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.car.is_available = True
        self.car.save()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"Rented {self.car} by {self.user.username}"
