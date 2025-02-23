from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    ACCOUNT_TYPES = [
        ("REFURB", "Refurbisher"),
        ("RECYCLE", "Recycler"),
    ]

    dob = models.CharField(max_length=10, default='1970-01-01')
    seller_rating = models.IntegerField(null=True, blank=True)
    accountType = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='sustainability_user_set',  # Updated related_name
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions '
                   'granted to each of their groups.'),
        related_query_name='user',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='sustainability_user_set',  # Updated related_name
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='user',
    )

    def get_listings(self):
        return Device.objects.filter(listing_user=self)

    def __str__(self):
        return f"{self.username} ({self.accountType})"

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
    listing_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Updated to use AUTH_USER_MODEL

    def __str__(self):
        return f"{self.deviceType}, {self.manufacturer}, {self.model}: {self.year}, {self.condition}: {self.price}$"

class Purchase(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    lister = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="sales", on_delete=models.CASCADE)  # Updated
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="purchases", on_delete=models.CASCADE)  # Updated
    purchaseDate = models.CharField(max_length=10)

    @property
    def seller(self):
        return self.lister

    @property
    def buyer_name(self):
        return f"{self.buyer.first_name} {self.buyer.last_name}"

    def __str__(self):
        return f"{self.buyer_name} bought {self.device} from {self.seller.first_name} on {self.purchaseDate}"
