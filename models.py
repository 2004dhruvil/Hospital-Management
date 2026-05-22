from django.db import models
from django.contrib.auth.models import User


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.IntegerField()
    specialization = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='doctor_profile')

    def __str__(self):
        return self.name
    
class Patient(models.Model):
    name = models.CharField(max_length=100)
    gender =models.CharField(max_length=10)
    mobile = models.IntegerField(null=True)
    address= models.CharField(max_length=150)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='patient_profile')

    def __str__(self):
        return self.name

class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date1 = models.DateField()
    time1 = models.TimeField()

    STATUS_CHOICES = (
        ("Pending", "Pending"),
        ("Scheduled", "Scheduled"),
        ("Rejected", "Rejected"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    
    # New fields for enhanced appointment management
    doctor_notes = models.TextField(blank=True, null=True, help_text="Notes for the patient")
    preparation_instructions = models.TextField(blank=True, null=True, help_text="Instructions for patient preparation")
    accepted_at = models.DateTimeField(blank=True, null=True, help_text="When doctor accepted the appointment")
    completed_at = models.DateTimeField(blank=True, null=True, help_text="When appointment was completed")

    def __str__(self):
        return f"{self.doctor.name} -- {self.patient.name} ({self.status})"


class DoctorAvailability(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('booked', 'Booked'),
        ('cancelled', 'Cancelled'),
    ]

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')

    def __str__(self):
        return f"{self.doctor.name} @ {self.date} {self.time} — {self.status}"
