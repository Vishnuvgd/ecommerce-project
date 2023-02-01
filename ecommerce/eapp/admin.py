from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(regmodel)
admin.site.register(shopregmodel)
admin.site.register(uploadmodel)
admin.site.register(addcartmodel)