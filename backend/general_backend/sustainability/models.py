from django.db import models

class Device(models.Model):
    DEVICE_TYPES = [
        ("PHONE", "Phone"), 
        ("LAPTOP", "Laptop"),
        ("TABLET", "Tablet"),
    ]
    CONDITION_TYPES = [
        ("BRAND NEW", "Brand new, never used"),
        ("GOOD", "Good condition, minimal usage"),
        ("AVERAGE USE", "Used condition, some normal wear and tear"),
        ("WORN", "Visible wear and tear, not the best condition"),
        ("POOR", "Lots of wear and tear which greatly inhibit device's performance"),
        ("BROKEN", "Broken and not in working order"),
    ]

    manufacturer = models.CharField(max_length=30)
    model = models.CharField(max_length=50)
    deviceType = models.CharField(max_length=6, choices=DEVICE_TYPES)
    year = models.IntegerField()
    size = models.CharField(max_length=40)
    condition = models.CharField(max_length=30, choices=CONDITION_TYPES)
    price = models.FloatField()
    listing_user = models.ForeignKey('User', on_delete=models.CASCADE)  # user who uploaded listing

    def __str__(self):
        return f"{self.deviceType}, {self.manufacturer}, {self.model}: {self.year}, {self.condition}: {self.price}$"


class User(models.Model):
    ACCOUNT_TYPES = [
        ("REFURB", "Refurbisher"),
        ("RECYCLE", "Recycler"),
    ]
        
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(primary_key=True)
    dob = models.CharField(max_length=10)
    seller_rating = models.IntegerField()
    accountType = models.CharField(max_length=20, choices=ACCOUNT_TYPES)

    def get_listings(self):
        listings = Device.objects.filter(listing_user=self)
        return listings

    def __str__(self):
        if self.accountType == "REFURB":
            return f"{self.first_name} {self.last_name}, DOB: {self.dob}, Email: {self.email}, Refurbisher - Seller rating: {self.seller_rating}"
        else:
            return f"{self.first_name} {self.last_name}, DOB: {self.dob}, Email: {self.email}, Recycler"


class Purchase(models.Model):
    device = models.ForeignKey('Device', on_delete=models.CASCADE)
    lister = models.ForeignKey('User', related_name="sales", on_delete=models.CASCADE)  #refurbisher
    buyer = models.ForeignKey('User', related_name="purchases", on_delete=models.CASCADE)  #
    purchaseDate = models.CharField(max_length=10)

    @property
    def seller(self):
        return self.lister

    @property
    def buyer_name(self):
        return f"{self.buyer.first_name} {self.buyer.last_name}"

    def __str__(self):
        return f"{self.buyer_name} bought {self.device} from {self.seller.first_name} on {self.purchaseDate}"
