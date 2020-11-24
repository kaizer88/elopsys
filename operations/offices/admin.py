from django.contrib import admin
from .forms import RegionForm, BranchForm, FloorForm, SectionForm, DepartmentForm
from .models import Region, Branch, Floor, Section, Department

# Register your models here.
class RegionAdmin(admin.ModelAdmin):
	list_display = ["__unicode__", "prefix", "id"]
	form = RegionForm
	#class Meta:
	#	model=SignUp

admin.site.register(Region, RegionAdmin)

	
class BranchAdmin(admin.ModelAdmin):
	list_display = ["__unicode__", "prefix", "region","id"]
	form = BranchForm
	#class Meta:
	#	model=SignUp

admin.site.register(Branch, BranchAdmin)


class FloorAdmin(admin.ModelAdmin):
	list_display = ["__unicode__", "branch", "id"]
	form = FloorForm
	#class Meta:
	#	model=SignUp

admin.site.register(Floor, FloorAdmin)

class SectionAdmin(admin.ModelAdmin):
	list_display = ["__unicode__", "floor", "id"]
	form = SectionForm
	#class Meta:
	#	model=SignUp

admin.site.register(Section, SectionAdmin)

class DepartmentAdmin(admin.ModelAdmin):
	list_display = ["__unicode__", "prefix", "id"]
	form = DepartmentForm
	#class Meta:
	#	model=SignUp

admin.site.register(Department, DepartmentAdmin)