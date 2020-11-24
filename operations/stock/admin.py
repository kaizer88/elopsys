from django.contrib import admin

# Register your models here.
from stock.models import *
from stock.forms import *

class ApplicationBookAdmin(admin.ModelAdmin):
	list_display = ["__unicode__", "written_by", "quantity"]
	form = BookForm
admin.site.register(Book, ApplicationBookAdmin)