from django.contrib import admin
from models import Light
# Register your models here.

class LightAdmin(admin.ModelAdmin):
    pass


admin.site.register(Light, LightAdmin)