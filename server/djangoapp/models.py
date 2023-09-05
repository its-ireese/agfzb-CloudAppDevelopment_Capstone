from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    make_name = models.CharField(null=False, max_length=48)
    make_description = models.CharField(null=True, max_length=480)

    def __str__(self):
        return self.make_name

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    model_make = models.ForeignKey(
        CarMake, null=True, on_delete=models.CASCADE)
    model_name = models.CharField(null=False, max_length=50)
    dealer_id = models.IntegerField(null=True)

    SEDAN = "Sedan"
    SUV = "SUV"
    COUPE = "Coupe"
    WAGON = "Wagon"
    PICKUP = "Pickup"
    MINIVAN = "Minivan"

    CAR_CHOICES = [(SEDAN, "Sedan"), (SUV, "SUV"), (COUPE, "Coupe"), (MINIVAN, "Minivan"),
                   (WAGON, "Wagon"), (PICKUP, "Pick-up truck")]
    model_type = models.CharField(
        null=False, max_length=15, choices=CAR_CHOICES, default=SEDAN)

    YEAR_CHOICES = []
    for r in range(2005, (datetime.datetime.now().year+1)):
        YEAR_CHOICES.append((r, r))

    model_year = models.IntegerField(
        ('year'), choices=YEAR_CHOICES, default=datetime.datetime.now().year)

    def __str__(self):
        return self.model_name + ", " + str(self.model_year) + ", " + self.model_type


# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, address=None, city=None, full_name=None, dealer_id=None, lat=None, long=None, short_name=None, state=None, st=None, zip=None):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.dealer_id = dealer_id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.state = state
        # Dealer state Short
        self.st = st
        # Dealer zip
        self.zip = zip

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, dealership=None, review_id=None, name=None, purchase=None, review=None, car_make=None, car_model=None, car_year=None, purchase_date=None, sentiment="neutral"):
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.dealership = dealership
        self.review_id = review_id
        self.name = name
        self.purchase = purchase
        self.purchase_date = purchase_date
        self.review = review
        self.sentiment = sentiment

    def __str__(self):
        return "Reviewer: " + self.name + " Review: " + self.review