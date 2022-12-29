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


class CarDealer:
    def __init__(
        self,
        id,
        address,
        city,
        full_name,
        state,
        # lat,
        # long,
        # short_name,
        # st,
            zip):
        # Dealer address
        self.address = address
        # # Dealer city
        self.city = city
        # # Dealer Full Name
        self.full_name = full_name
        # # Dealer id
        self.id = id
        # # Location lat
        # self.lat = lat
        # # Location long
        # self.long = long
        # # Dealer short name
        # self.short_name = short_name
        # # Dealer state
        # self.st = st
        # # Dealer zip
        self.zip = zip
        self.state = state

    def __str__(self):
        return self.full_name


class DealerReview:
    def __init__(
            self,
            dealership,
            name,
            purchase,
            review,
            purchase_date,
            car_make,
            car_model,
            car_year,
            sentiment,
            id):
        # Dealer id
        self.dealership = dealership
        # Reviewer name
        self.name = name
        # Car purchase
        self.purchase = purchase
        # Review text
        self.review = review
        # Purchase date
        self.purchase_date = purchase_date
        # Car make
        self.car_make = car_make
        # Car model
        self.car_model = car_model
        # Car year
        self.car_year = car_year
        # Review sentiment
        self.sentiment = sentiment
        # Review id
        self.id = id

    def __str__(self):
        return "Review: " + self.review
