"""
Email notification system for appointment updates
"""

from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import datetime

def send_appointment_notification(appointment, action_type):
    """Send email notification to patient about appointment status change"""
    
    patient = appointment.patient
    doctor = appointment.doctor
    
    # Email templates based on action type
    subject_templates = {
        'accepted': f"Appointment Confirmed - {doctor.name}",
        'rejected': f"Appointment Update - {doctor.name}",
        'completed': f"Appointment Completed - {doctor.name}",
        'cancelled': f"Appointment Cancelled - {doctor.name}"
    }
    
    subject = subject_templates.get(action_type, "Appointment Update")
    
    # Email content
    context = {
        'patient_name': patient.name,
        'doctor_name': doctor.name,
        'appointment_date': appointment.date1,
        'appointment_time': appointment.time1,
        'action_type': action_type,
        'doctor_notes': appointment.doctor_notes,
        'preparation_instructions': appointment.preparation_instructions,
    }
    
    # Create email message
    message = f"""
Dear {patient.name},

Your appointment with Dr. {doctor.name} has been {action_type}.

Appointment Details:
- Date: {appointment.date1}
- Time: {appointment.time1}
- Status: {appointment.status}

"""
    
    if appointment.doctor_notes:
        message += f"Doctor's Notes: {appointment.doctor_notes}\n\n"
    
    if appointment.preparation_instructions:
        message += f"Preparation Instructions: {appointment.preparation_instructions}\n\n"
    
    message += """
Please contact the hospital if you have any questions.

Best regards,
Hospital Management System
"""
    
    # Send email (only if email is configured)
    if hasattr(settings, 'EMAIL_HOST') and settings.EMAIL_HOST:
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [patient.user.email] if patient.user and patient.user.email else [],
                fail_silently=True,
            )
            return True
        except Exception as e:
            print(f"Email sending failed: {e}")
            return False
    return False

def send_appointment_reminder(appointment):
    """Send reminder email 24 hours before appointment"""
    
    patient = appointment.patient
    doctor = appointment.doctor
    
    subject = f"Appointment Reminder - Tomorrow with Dr. {doctor.name}"
    
    message = f"""
Dear {patient.name},

This is a reminder that you have an appointment tomorrow:

Appointment Details:
- Doctor: Dr. {doctor.name}
- Date: {appointment.date1}
- Time: {appointment.time1}

"""
    
    if appointment.preparation_instructions:
        message += f"Preparation Instructions: {appointment.preparation_instructions}\n\n"
    
    message += """
Please arrive 15 minutes early for your appointment.

Best regards,
Hospital Management System
"""
    
    # Send reminder email
    if hasattr(settings, 'EMAIL_HOST') and settings.EMAIL_HOST:
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [patient.user.email] if patient.user and patient.user.email else [],
                fail_silently=True,
            )
            return True
        except Exception as e:
            print(f"Reminder email failed: {e}")
            return False
    return False

