from django.contrib import admin

# Register your models here.
from .forms import VehicleMakeAndModelForm, VehicleExtrasForm, addNewVehicleForm
from .models import VehicleMakeAndModel, VehicleExtras,Vehicle


class VehicleMakeAndModelAdmin(admin.ModelAdmin):
	list_display = ["__unicode__", "make_n_model", "vehicle_class", "engine_capacity", "transmission_type"]
	form = VehicleMakeAndModelForm

admin.site.register(VehicleMakeAndModel, VehicleMakeAndModelAdmin)

class VehicleExtrasAdmin(admin.ModelAdmin):
	list_display = ["__unicode__", "make_n_model"]
	form = VehicleExtrasForm

admin.site.register(VehicleExtras, VehicleExtrasAdmin)

class VehicleAdmin(admin.ModelAdmin):
	list_display = ["__unicode__", "make_n_model", 'model_year', 'color', 'ownership_type']
	form = addNewVehicleForm

admin.site.register(Vehicle, VehicleAdmin)

	
