from django.contrib import admin
from .models import SchoolModel
# Register your models here.

class SchoolModelAdmin(admin.ModelAdmin):
    list_display = ["name", "start_date", "distance"]
admin.site.register(SchoolModel, SchoolModelAdmin)