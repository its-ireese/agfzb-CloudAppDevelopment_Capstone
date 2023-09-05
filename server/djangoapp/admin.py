from django.contrib import admin
# from .models import related models
from .models import CarModel, CarMake

# Register your models here.

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 2

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['model_make', 'model_name',
                    'dealer_id', 'model_type', 'model_year']
    list_filter = ['model_type', 'model_make', 'dealer_id', 'model_year', ]
    search_fields = ['model_make', 'model_name']

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ['make_name', 'make_description']
    search_fields = ['make_name']
    inlines = [CarModelInline]

# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)