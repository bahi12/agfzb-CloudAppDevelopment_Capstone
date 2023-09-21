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
        verbose_name =("Car Make")
        verbose_name_plural =("Car Makes")

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
    make = models.ForeignKey(CarMake , on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=250)
    dealer_id = models.IntegerField()
    type = CarTypeField(max_length=255)
    year = models.DateField(default=datetime.date.today().year)  
      
    def __str__(self):
        return self.name

    class Meta:
        verbose_name =("Car Model")
        verbose_name_plural =("Car Models")

    def get_absolute_url(self):
        return reverse("CarModel_detail", kwargs={"pk": self.pk})


# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
