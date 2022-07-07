from django.contrib import admin

from seller.models import *

# Register your models here.

#admin.site.register(seller)

@admin.register(seller)
class UserAdmin(admin.ModelAdmin):
    list_display= ['name','mobile','email','password','pic']

@admin.register(Product)
class UserAdmin(admin.ModelAdmin):
    list_display= ['name','des','price','quantity','discount','pic','seller','discountedprice']