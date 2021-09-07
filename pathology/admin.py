from django.contrib import admin
from . import models
# Register your models here.
@admin.register(models.Doctor)
class DoctorAdmin(admin.ModelAdmin):
    
    list_display = ['id','iddentificationID','name','created_at']
    # list_editable = ['iddentificationID','name']
    ordering = ['created_at','name']
    search_fields = ['name__istartswith','iddentificationID__istartswith']
    list_per_page = 10