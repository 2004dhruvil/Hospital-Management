from django.contrib import admin
from .models import *

# Custom Admin Classes with Filters
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['name', 'specialization', 'mobile', 'user']
    list_filter = ['specialization', 'user__is_active']
    search_fields = ['name', 'specialization', 'mobile']
    list_per_page = 20
    ordering = ['name']

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['name', 'gender', 'mobile', 'address', 'user']
    list_filter = ['gender', 'user__is_active']
    search_fields = ['name', 'mobile', 'address']
    list_per_page = 20
    ordering = ['name']

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'patient', 'date1', 'time1', 'status']
    list_filter = ['status', 'date1', 'doctor__specialization']
    search_fields = ['doctor__name', 'patient__name']
    list_per_page = 20
    ordering = ['-date1', '-time1']
    date_hierarchy = 'date1'

@admin.register(DoctorAvailability)
class DoctorAvailabilityAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'date', 'time']
    list_filter = ['date', 'doctor__specialization']
    search_fields = ['doctor__name']
    list_per_page = 20
    ordering = ['date', 'time']
    date_hierarchy = 'date'