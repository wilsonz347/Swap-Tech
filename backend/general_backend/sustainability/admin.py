#backend/admin.py

from django.contrib import admin
from .models import User, Device, Purchase

admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')
    search_fields = ('first_name', 'last_name', 'email')

admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'deviceType')
    search_fields = ('name',)

admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('device', 'lister', 'buyer', 'purchaseDate')
    list_filter = ('purchaseDate',)
    search_fields = ('device__name', 'lister__first_name', 'buyer__first_name')
