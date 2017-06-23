from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import *

admin.site.register(Password)
admin.site.register(PendingDeviceRequest)
admin.site.register(AuthorizedToken)