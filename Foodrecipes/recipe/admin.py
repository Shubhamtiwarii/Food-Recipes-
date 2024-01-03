from django.contrib import admin
from .models import *

class ProductAdmin(admin.ModelAdmin):
    list_display=['name','price','description','category']

class CategoryAdmin(admin.ModelAdmin):
    list_display=['name']
class CustomerAdmin(admin.ModelAdmin):
    list_display=['first_name','last_name','email','password','phone']

class OrderAdmin(admin.ModelAdmin):
    list_display=['product','customer','quantity','price','date']
admin.site.register(Product,ProductAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Customer,CustomerAdmin)
#admin.site.register(Order)
admin.site.register(Order,OrderAdmin)