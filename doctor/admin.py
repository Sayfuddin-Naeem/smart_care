from django.contrib import admin
from .models import (
    Specialization,
    Designation,
    AvailableTime,
    Doctor,
    Review
)
# Register your models here.
@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',),}
    list_display = ['name', 'slug']
    
@admin.register(Designation)
class DesignationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',),}
    list_display = ['name', 'slug']

admin.site.register(AvailableTime)
admin.site.register(Doctor)
admin.site.register(Review)
    