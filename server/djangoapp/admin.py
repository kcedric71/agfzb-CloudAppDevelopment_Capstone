from django.contrib import admin
from .models import CarMake, CarModel

# Register your models here.

# CarModelInline class
class CarModelInLine(admin.StackedInline):
    model = CarModel
    extra = 1

# CarModelAdmin class
#class CarModelAdmin(admin.ModelAdmin):

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInLine]

# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel)
