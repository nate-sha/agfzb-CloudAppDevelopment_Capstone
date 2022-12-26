from django.db import models
from django.utils.timezone import now

# Generate a random hex string for the id (primary key)
from djangoapp.utils.hex_id import generate_hex

# Create your models here.


class CarMake(models.Model):
    id = models.CharField(primary_key=True, max_length=8, default=generate_hex)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    CAR_TYPES = (
        ('Sedan', 'Sedan'),
        ('SUV', 'SUV'),
        ('Truck', 'Truck'),
        ('Coupe', 'Coupe'),
        ('WAGON', 'WAGON'),
    )
    id = models.CharField(primary_key=True, max_length=8, default=generate_hex)
    name = models.CharField(max_length=50)
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=CAR_TYPES)
    dealer_id = models.IntegerField()
    year = models.DateField()

    def __str__(self):
        return self.name


# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
