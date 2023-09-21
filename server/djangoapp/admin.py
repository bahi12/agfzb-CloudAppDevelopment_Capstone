from django.contrib import admin
# from .models import related models
from .models import CarMake, CarModel


# Register your models here.

# CarModelInline class
class CarModelInLine(admin.TabularInline):
    model = CarModel
    extra = 3
# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    fields = ("name", "make", "type", "year")
# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInLine]
# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
