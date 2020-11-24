from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
from employees.models import *

# Create your models here.


class ElopsysUser(AbstractUser):
	class Meta:
		db_table = "elopsys_user"

	phone_number = models.CharField(null=True, max_length=50)
	employee = models.ForeignKey('employees.Employee', null=True, blank=True)   
	designation = models.ForeignKey('employees.Designation', null=True, blank=True)
	signature = models.FileField(null=True, blank=True, upload_to='uploads/accounts')
	regional_staff = models.BooleanField(blank=True, default=False)


	def __unicode__(self):
		return self.username


	def fullname(self):
		return self.first_name+" "+self.last_name

	@property
	def can_edit(self):
		return self.is_superuser or self.privilege == 'create_elopsysuser' or self.privilege == 'admin'

	@property
	def is_executive(self):
		return 'Operations Executive' in self.groups.all()