from django.db import models
from django.utils.timezone import now
import datetime
from django.urls import reverse

# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object


class CarMake(models.Model):
    name = models.CharField(null=False, max_length=255)
    description = models.TextField()

    class Meta:
        verbose_name = ("Car Make")
        verbose_name_plural = ("Car Makes")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("CarMake_detail", kwargs={"pk": self.pk})

    def get_absolute_url(self):
        return reverse("CarMake_detail", kwargs={"pk": self.pk})


class CarTypeField(models.CharField):
    def get_choices(self):
        car_makes = CarMake.objects.all()
        choices = [(car_make.name, car_make.name) for car_make in car_makes]
        return choices
# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object


class CarModel(models.Model):
    # Many-To-One relationship to Car Make model
    make = models.ForeignKey('CarMake', on_delete=models.CASCADE)

    # Name of the car model
    name = models.CharField(max_length=250)

    # Dealer id, used to refer a dealer created in cloudant database
    id = models.IntegerField(default=1, primary_key=True)

    # Type of the car (choices argument provides limited options)
    CAR_TYPES = [
        ('Sedan', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'WAGON'),
        ('Convertible', 'Convertible'),
        ('Coupe', 'Coupe'),
        ('Hatchback', 'Hatchback'),
        ('Truck', 'Truck'),
        ('Van', 'Van'),
        # Add other types as needed
    ]
    type = models.CharField(max_length=255, choices=CAR_TYPES)

    # Year of the car
    year = models.DateField()

    # Any other fields you would like to include in car model

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Car Model"
        verbose_name_plural = "Car Models"

    def get_absolute_url(self):
        return reverse("CarModel_detail", kwargs={"pk": self.pk})

# <HINT> Create a plain Python class `CarDealer` to hold dealer data


class CarDealer:

    def __init__(self, address, city, id, lat, long, st, zip, full_name):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city

        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long

        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

        # Full name
        self.full_name = full_name

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data


class DealerReview:
    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, id, sentiment=None):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment  # Watson NLU service
        self.id = id

    def __str__(self):
        return "Review: " + self.review +\
            " Sentiment: " + self.sentiment
