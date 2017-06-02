from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
# Create your models here.
class Password(models.Model):
	name = models.CharField(max_length = 100,primary_key = True)
	password = models.CharField(max_length = 100)
	date_created = models.DateTimeField(default = timezone.now)
	def __str__(self):
		return self.name
	def clean(self):
		if len(self.name) == 0 or len(self.password) == 0:
			raise ValidationError(_("Empty fields"))
		if len(self.name.strip()) == 0 or len(self.password.strip()) == 0:
			raise ValidationError(_("Invalid name or password"))
