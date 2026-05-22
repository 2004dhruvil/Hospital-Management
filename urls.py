# """
# URL configuration for HospitalManagement project.

# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/5.2/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """

# from django.contrib import admin
# from django.urls import path
# from hospital.views import *


# urlpatterns = [
#     path("admin/", admin.site.urls),
#     path("about/",About,name='about'),
#     path("contact/",Contact,name='contact'),
#     # role selection as home
#     path("", role_select, name='role_select'),
#     # keep admin dashboard at /home
#     path("home/",Index,name='home'),
#     # admin login unchanged path alias kept
#     path("admin_login/",Login,name='login'),
#     # doctor & patient auth
#     path("doctor/login/", doctor_login, name='doctor_login'),
#     path("patient/login/", patient_login, name='patient_login'),
#     path("patient/register/", patient_register, name='patient_register'),
#     path("doctor/dashboard/", doctor_dashboard, name='doctor_dashboard'),
#     path("patient/dashboard/", patient_dashboard, name='patient_dashboard'),
#     path("doctor/appointments/", doctor_appointments, name='doctor_appointments'),
#     path('doctor/accept/<int:aid>/', doctor_accept_appointment, name='doctor_accept_appointment'),
#     path('doctor/reject/<int:aid>/', doctor_reject_appointment, name='doctor_reject_appointment'),
#     path('doctor/complete/<int:aid>/', doctor_complete_appointment, name='doctor_complete_appointment'),

#     path("patient/appointments/", patient_appointments, name='patient_appointments'),
#     path("patient/book/", patient_book_appointment, name='patient_book_appointment'),
#     path("patient/profile/", patient_profile, name='patient_profile'),
#     path("doctor/profile/", doctor_profile, name='doctor_profile'),
#     path("doctor/availability/", doctor_availability, name='doctor_availability'),
#     path("patient/appointments/<int:aid>/cancel/", patient_cancel_appointment, name='patient_cancel_appointment'),
#     path("patient/appointments/<int:aid>/reschedule/", patient_reschedule_appointment, name='patient_reschedule_appointment'),
#     path("doctor/appointments/<int:aid>/complete/", doctor_complete_appointment, name='doctor_complete_appointment'),
#     path("logout/",Logout_admin,name='logout'),
#     path("view_doctor/", View_Doctor,name='view_doctor'),
#     path("add_doctor/", Add_Doctor,name='add_doctor'),
#     path("delete_doctor(?P<int:pid>)", Delete_Doctor,name='delete_doctor'),
#     path("view_patient/", View_Patient,name='view_patient'),
#     path("add_patient/", Add_Patient,name='add_patient'),
#     path("delete_patient(?P<int:pid>)", Delete_Patient,name='delete_patient'),
#     path("view_appointment/", View_Appointment,name='view_appointment'),
#     path("add_appointment/", Add_Appointment,name='add_appointment'),
#     path("delete_appointment(?P<int:pid>)", Delete_Appointment,name='delete_appointment'),




#     # path('', home, name='home'),
# ]


from django.contrib import admin
from django.urls import path
from hospital.views import *

urlpatterns = [
    path("admin/", admin.site.urls),

    # Static pages
    path("about/", About, name='about'),
    path("contact/", Contact, name='contact'),

    # Home & role selection
    path("", role_select, name='role_select'),        # default home = role select
    path("home/", Index, name='home'),                # admin dashboard
    path("admin_login/", Login, name='login'),        # admin login

    # Doctor & Patient Auth
    path("doctor/login/", doctor_login, name='doctor_login'),
    path("patient/login/", patient_login, name='patient_login'),
    path("patient/register/", patient_register, name='patient_register'),

    # Dashboards
    path("doctor/dashboard/", doctor_dashboard, name='doctor_dashboard'),
    path("patient/dashboard/", patient_dashboard, name='patient_dashboard'),

    # Doctor Appointments
    path("doctor/appointments/", doctor_appointments, name='doctor_appointments'),
    path("doctor/appointments/<int:aid>/accept/", doctor_accept_appointment, name='doctor_accept_appointment'),
    path("doctor/appointments/<int:aid>/reject/", doctor_reject_appointment, name='doctor_reject_appointment'),
    path("doctor/appointments/<int:aid>/complete/", doctor_complete_appointment, name='doctor_complete_appointment'),

    # Patient Appointments
    path("patient/appointments/", patient_appointments, name='patient_appointments'),
    path("patient/book/", patient_book_appointment, name='patient_book_appointment'),
    path("patient/appointments/<int:aid>/cancel/", patient_cancel_appointment, name='patient_cancel_appointment'),
    path("patient/appointments/<int:aid>/reschedule/", patient_reschedule_appointment, name='patient_reschedule_appointment'),
    path("get-slots/", get_doctor_slots, name="get_doctor_slots"),

    # Profiles
    path("patient/profile/", patient_profile, name='patient_profile'),
    path("doctor/profile/", doctor_profile, name='doctor_profile'),
    path("doctor/availability/", doctor_availability, name='doctor_availability'),

    # Admin logout
    path("logout/", Logout_admin, name='logout'),

    # Admin: manage doctors/patients/appointments
    path("view_doctor/", View_Doctor, name='view_doctor'),
    path("add_doctor/", Add_Doctor, name='add_doctor'),
    path("delete_doctor/<int:pid>/", Delete_Doctor, name='delete_doctor'),

    path("view_patient/", View_Patient, name='view_patient'),
    path("add_patient/", Add_Patient, name='add_patient'),
    path("delete_patient/<int:pid>/", Delete_Patient, name='delete_patient'),

    path("view_appointment/", View_Appointment, name='view_appointment'),
    path("add_appointment/", Add_Appointment, name='add_appointment'),
    path("delete_appointment/<int:pid>/", Delete_Appointment, name='delete_appointment'),

    path('session/', show_session, name='show_session'),
    path('cookies/', show_cookies, name='show_cookies'),

]
