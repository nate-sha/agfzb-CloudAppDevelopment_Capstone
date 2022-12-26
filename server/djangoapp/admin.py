from django.contrib import admin
from .models import CarMake, CarModel

# Change the admin site header
admin.site.site_header = "Best Dealership Admin"


class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 0


class CarModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'car_make', 'type', 'dealer_id', 'year')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'type')
    list_per_page = 25


class CarMakeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description',)
    list_display_links = ('id', 'name')
    search_fields = ('name', 'description')
    list_per_page = 25
    inlines = [CarModelInline]


admin.site.register(CarMake, CarMakeAdmin)
