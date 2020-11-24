from django.contrib import admin

# Register your models here.
from offices.models import *
from .models import *
from .forms import *

class MeterNumberAdmin(admin.ModelAdmin):
	list_display = ["__unicode__", "meter_number", 'branch']
	form = ElectricityMeterNumberForm

admin.site.register(ElectricityMeterNumber, MeterNumberAdmin)
