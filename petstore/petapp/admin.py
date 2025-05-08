from django.contrib import admin
from petapp.models import Pet,Cart, Order
# Register your models here.


class PetAdmin(admin.ModelAdmin):  # this will create 
    list_display=['id','name','age','breed','type','price','gender', 'details', 'img']
    list_filter=['type','price']

admin.site.register(Pet,PetAdmin)


class CartAdmin(admin.ModelAdmin):
    list_display=['id','uid','pid','quantity']

admin.site.register(Cart,CartAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display=['id','orderid','userid','petid','quantity','totallBill']
    


admin.site.register(Order,OrderAdmin)

