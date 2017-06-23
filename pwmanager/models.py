from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
import string
import random

def random_code(length = 256):
	return ''.join([random.choice(string.ascii_letters + string.digits) for i in range(length)])

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

class PendingDeviceRequest(models.Model):
	code = models.CharField(max_length = 256,primary_key = True,default = random_code)
	# verified = models.BooleanField(default = False)
	date_created = models.DateTimeField(default = timezone.now)
	def __str__(self):
		return self.code
	def verify(self):
		self.verified = True
		self.save()

class AuthorizedToken(models.Model):
	token = models.CharField(max_length = 256,primary_key = True,default = random_code)
	expiry_date = models.DateTimeField(null = True, default = None)
	def __str__(self):
		return self.token

	@staticmethod
	def create_and_get_token(expiry_date = None):
		auth = AuthorizedToken(expiry_date = expiry_date)
		token = auth.token
		auth.save()
		return token

	@staticmethod
	def is_valid_token(token):
		return AuthorizedToken.objects.filter(expiry_date__st = timezone.now,token = token).exists()
