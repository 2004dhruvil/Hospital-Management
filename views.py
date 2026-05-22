from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from .models import *
from django.conf import settings
from datetime import timedelta

# ---------- STATIC PAGES ----------
def About(request):
    return render(request, 'about.html')

def Contact(request):
    return render(request, 'contact.html')

# ---------- ADMIN DASHBOARD ----------
def Index(request):
    if not request.user.is_staff:
        return redirect('login')
    doctors = Doctor.objects.count()
    patients = Patient.objects.count()
    appointments = Appointment.objects.count()
    d1 = {'d': doctors, 'p': patients, 'a': appointments}
    return render(request, 'index.html', d1)

# ---------- ADMIN LOGIN ----------
def Login(request):
    error = ""
    session_data = {}
    cookies = {}

    if request.method == 'POST':
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)

        if user is not None and user.is_staff:
            login(request, user)
            
            # Session setup
            request.session['role'] = 'admin'
            request.session.set_expiry(60 * 60 * 6)  # 6 hours

            # Prepare response for rendering (no redirect)
            error = "no"

            # Create a temporary response for cookies display
            resp = render(request, 'login.html', {
                'error': error,
                'session_data': dict(request.session),
                'cookies': request.COOKIES
            })

            # Set cookie for role
            cookie_name = f"{getattr(settings, 'APP_COOKIE_PREFIX', 'hms_')}role"
            resp.set_cookie(
                key=cookie_name,
                value='admin',
                max_age=60 * 60 * 6,
                secure=not settings.DEBUG,
                httponly=False,
                samesite='Lax',
            )

            print("✅ Admin logged in successfully.")
            print("Session Data:", dict(request.session))
            print("Cookies:", request.COOKIES)
            return resp

        else:
            error = "yes"

    # Normal render (GET request or failed login)
    return render(request, 'login.html', {
        'error': error,
        'session_data': dict(request.session),
        'cookies': request.COOKIES
    })

def Logout_admin(request):
    logout(request)
    resp = redirect('role_select')
    # clear role cookie
    resp.delete_cookie(f"{getattr(settings, 'APP_COOKIE_PREFIX', 'hms_')}role")
    return resp

# ---------- ROLE SELECTION ----------
def role_select(request):
    return render(request, 'role_select.html')




# ---------- DOCTOR LOGIN ----------
def doctor_login(request):
    error = ""

    if request.method == 'POST':
        username_raw = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        secret = request.POST.get('secret', '').strip()

        # Expected doctor secret key from settings.py
        expected_secret = getattr(settings, 'DOCTOR_SECRET_KEY', '')

        # Validate secret key
        if secret != expected_secret:
            error = "secret"
        else:
            user_obj = User.objects.filter(username__iexact=username_raw).first()
            auth_username = user_obj.username if user_obj else username_raw
            user = authenticate(username=auth_username, password=password)

            if user is None:
                error = "creds"
            elif not hasattr(user, 'doctor_profile'):
                error = "profile"
            else:
                # Login success
                login(request, user)

                # Set session data
                request.session['role'] = 'doctor'
                request.session.set_expiry(60 * 60 * 12)  # 12 hours

                # Create redirect response
                resp = redirect('doctor_dashboard')

                # Set cookie for role
                cookie_name = f"{getattr(settings, 'APP_COOKIE_PREFIX', 'hms_')}role"
                resp.set_cookie(
                    key=cookie_name,
                    value='doctor',
                    max_age=60 * 60 * 12,
                    secure=not settings.DEBUG,
                    httponly=False,
                    samesite='Lax',
                )

                # Debug info in terminal
                print("✅ Doctor logged in successfully.")
                print("Session Data:", dict(request.session))
                print("Cookies:", request.COOKIES)

                return resp

    # Render login page with debug info
    return render(request, 'doctor_login.html', {
        'error': error,
        'session_data': dict(request.session),
        'cookies': request.COOKIES
    })

# ---------- PATIENT REGISTER/LOGIN ----------
def patient_register(request):
    error = ""
    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        gender = request.POST.get('gender')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')

        if User.objects.filter(username=username).exists():
            error = "exists"
        else:
            try:
                user = User.objects.create_user(username=username, password=password, first_name=name)
                Patient.objects.create(name=name, gender=gender, mobile=mobile or None, address=address, user=user)
                login(request, user)
                request.session['role'] = 'patient'
                request.session.set_expiry(60 * 60 * 24 * 7)  # 1 week for patients
                resp = redirect('patient_dashboard')
                resp.set_cookie(
                    key=f"{getattr(settings, 'APP_COOKIE_PREFIX', 'hms_')}role",
                    value='patient',
                    max_age=60 * 60 * 24 * 7,
                    secure=not settings.DEBUG,
                    httponly=False,
                    samesite='Lax',
                )
                return resp
            except:
                error = "yes"
    return render(request, 'patient_register.html', {'error': error})

def patient_login(request):
    error = ""
    session_data = {}
    cookies = {}

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None and hasattr(user, 'patient_profile'):
            login(request, user)

            # Set session
            request.session['role'] = 'patient'
            request.session.set_expiry(60 * 60 * 24 * 7)  # 7 days

            # Prepare response (no redirect so debug info can show)
            error = "no"
            resp = render(request, 'patient_login.html', {
                'error': error,
                'session_data': dict(request.session),
                'cookies': request.COOKIES
            })

            # Set cookie for role
            cookie_name = f"{getattr(settings, 'APP_COOKIE_PREFIX', 'hms_')}role"
            resp.set_cookie(
                key=cookie_name,
                value='patient',
                max_age=60 * 60 * 24 * 7,
                secure=not settings.DEBUG,
                httponly=False,
                samesite='Lax'
            )

            print("✅ Patient logged in successfully.")
            print("Session Data:", dict(request.session))
            print("Cookies:", request.COOKIES)

            return resp
        else:
            error = "yes"

    # Render login page (GET request or failed login)
    return render(request, 'patient_login.html', {
        'error': error,
        'session_data': dict(request.session),
        'cookies': request.COOKIES
    })

# ---------- DASHBOARDS ----------
def doctor_dashboard(request):
    if not request.user.is_authenticated or not hasattr(request.user, 'doctor_profile'):
        return redirect('doctor_login')
    doctor = request.user.doctor_profile
    appointments = Appointment.objects.filter(doctor=doctor).order_by('date1', 'time1')
    ctx = {
        'doctor': doctor,
        'upcoming': appointments.count(),
        'patients_count': Patient.objects.filter(appointment__doctor=doctor).distinct().count(),
        'appointments': appointments[:5],
    }
    return render(request, 'doctor_dashboard.html', ctx)

def patient_dashboard(request):
    if not request.user.is_authenticated or not hasattr(request.user, 'patient_profile'):
        return redirect('patient_login')
    patient = request.user.patient_profile
    appointments = Appointment.objects.filter(patient=patient).order_by('date1', 'time1')
    ctx = {
        'patient': patient,
        'upcoming': appointments.count(),
        'doctors_count': Doctor.objects.filter(appointment__patient=patient).distinct().count(),
        'appointments': appointments[:5],
    }
    return render(request, 'patient_dashboard.html', ctx)

# ---------- APPOINTMENTS ----------
def doctor_appointments(request):
    if not request.user.is_authenticated or not hasattr(request.user, 'doctor_profile'):
        return redirect('doctor_login')
    doctor = request.user.doctor_profile
    appointments = Appointment.objects.filter(doctor=doctor).order_by('-date1', '-time1')
    return render(request, 'doctor_appointments.html', {'appointments': appointments})

def patient_appointments(request):
    if not request.user.is_authenticated or not hasattr(request.user, 'patient_profile'):
        return redirect('patient_login')
    patient = request.user.patient_profile
    appointments = Appointment.objects.filter(patient=patient).order_by('-date1', '-time1')
    return render(request, 'patient_appointments.html', {'appointments': appointments})

def patient_book_appointment(request):
    if not request.user.is_authenticated or not hasattr(request.user, 'patient_profile'):
        return redirect('patient_login')

    error = ""
    doctors = Doctor.objects.all()

    if request.method == 'POST':
        doctor_name = request.POST.get('doctor')   # doctor name
        slot_id = request.POST.get('slot')         # selected slot ID

        doctor = Doctor.objects.filter(name=doctor_name).first()
        patient = request.user.patient_profile

        # Fetch the selected slot
        slot = DoctorAvailability.objects.filter(id=slot_id, status="available").first()

        if doctor is None or slot is None:
            error = "yes"
        else:
            try:
                # Create appointment
                Appointment.objects.create(
                    doctor=doctor,
                    patient=patient,
                    date1=slot.date,
                    time1=slot.time,
                    status="Pending"
                )

                # Mark the slot as booked
                slot.status = "booked"
                slot.save()

                return redirect('patient_appointments')

            except:
                error = "yes"

    return render(request, 'patient_book_appointment.html', {
        'doctors': doctors,
        'error': error
    })

# ---------- DOCTOR ACTIONS ----------
def doctor_accept_appointment(request, aid):
    if not request.user.is_authenticated or not hasattr(request.user, 'doctor_profile'):
        return redirect('doctor_login')
    appt = get_object_or_404(Appointment, id=aid, doctor=request.user.doctor_profile)
    
    if request.method == "POST":
        # Update appointment status
        appt.status = "Scheduled"
        appt.accepted_at = timezone.now()
        
        # Get additional information from form
        doctor_notes = request.POST.get('doctor_notes', '')
        preparation_instructions = request.POST.get('preparation_instructions', '')
        
        appt.doctor_notes = doctor_notes
        appt.preparation_instructions = preparation_instructions
        appt.save()
        
        # Send notification email
        try:
            from .notifications import send_appointment_notification
            send_appointment_notification(appt, 'accepted')
        except:
            pass  # Continue even if email fails
        
        return redirect('doctor_appointments')
    
    return render(request, 'doctor_accept_appointment.html', {'appointment': appt})

def doctor_reject_appointment(request, aid):
    if not request.user.is_authenticated or not hasattr(request.user, 'doctor_profile'):
        return redirect('doctor_login')
    appt = get_object_or_404(Appointment, id=aid, doctor=request.user.doctor_profile)
    if request.method == "POST":
        appt.status = "Rejected"
        appt.save()
        return redirect('doctor_appointments')
    return render(request, 'doctor_reject_appointment.html', {'appointment': appt})

def doctor_complete_appointment(request, aid):
    if not request.user.is_authenticated or not hasattr(request.user, 'doctor_profile'):
        return redirect('doctor_login')
    appt = get_object_or_404(Appointment, id=aid, doctor=request.user.doctor_profile)
    if request.method == "POST":
        appt.status = "Completed"
        appt.save()
        return redirect('doctor_appointments')
    return render(request, 'doctor_complete_appointment.html', {'appointment': appt})

# ---------- AVAILABILITY ----------
def doctor_availability(request):
    if not request.user.is_authenticated or not hasattr(request.user, 'doctor_profile'):
        return redirect('doctor_login')

    doctor = request.user.doctor_profile
    success = False

    if request.method == 'POST':
        date = request.POST.get('date')
        time = request.POST.get('time')

        if date and time:
            DoctorAvailability.objects.create(
                doctor=doctor,
                date=date,
                time=time,
                # status is not passed → model default = "available"
            )
            success = True

    slots = DoctorAvailability.objects.filter(
        doctor=doctor
    ).order_by('date', 'time')

    return render(request, 'doctor_availability.html', {
        'slots': slots,
        'success': success
    })


from django.http import JsonResponse

def get_doctor_slots(request):
    doctor_name = request.GET.get("doctor")
    slots = []

    if doctor_name:
        from .models import Doctor, DoctorAvailability
        
        doctor = Doctor.objects.filter(name=doctor_name).first()
        if doctor:
            avail = DoctorAvailability.objects.filter(
                doctor=doctor,
                status="available"
            ).order_by("date", "time")
            
            for s in avail:
                slots.append({
                    "id": s.id,
                    "datetime": f"{s.date} {s.time}"
                })

    return JsonResponse({"slots": slots})

# ---------- PATIENT ACTIONS ----------
def patient_cancel_appointment(request, aid):
    if not request.user.is_authenticated or not hasattr(request.user, 'patient_profile'):
        return redirect('patient_login')
    appt = Appointment.objects.filter(id=aid, patient=request.user.patient_profile).first()
    if appt:
        appt.status = 'Cancelled'
        appt.save()
    return redirect('patient_appointments')

def patient_reschedule_appointment(request, aid):
    if not request.user.is_authenticated or not hasattr(request.user, 'patient_profile'):
        return redirect('patient_login')
    appt = Appointment.objects.filter(id=aid, patient=request.user.patient_profile).first()
    if not appt:
        return redirect('patient_appointments')
    error = ""
    if request.method == 'POST':
        date = request.POST.get('date')
        time = request.POST.get('time')
        try:
            appt.date1 = date
            appt.time1 = time
            appt.status = 'Scheduled'
            appt.save()
            return redirect('patient_appointments')
        except:
            error = "yes"
    return render(request, 'patient_reschedule.html', {'appointment': appt, 'error': error})

# ---------- PROFILES ----------
def patient_profile(request):
    if not request.user.is_authenticated or not hasattr(request.user, 'patient_profile'):
        return redirect('patient_login')
    patient = request.user.patient_profile
    success = False
    if request.method == 'POST':
        patient.name = request.POST.get('name')
        patient.gender = request.POST.get('gender')
        patient.mobile = request.POST.get('mobile') or None
        patient.address = request.POST.get('address')
        patient.save()
        request.user.first_name = patient.name
        request.user.save()
        success = True
    return render(request, 'patient_profile.html', {'patient': patient, 'success': success})

def doctor_profile(request):
    if not request.user.is_authenticated or not hasattr(request.user, 'doctor_profile'):
        return redirect('doctor_login')
    doctor = request.user.doctor_profile
    success = False
    if request.method == 'POST':
        doctor.name = request.POST.get('name')
        doctor.mobile = request.POST.get('mobile') or doctor.mobile
        doctor.specialization = request.POST.get('specialization')
        doctor.save()
        request.user.first_name = doctor.name
        request.user.save()
        success = True
    return render(request, 'doctor_profile.html', {'doctor': doctor, 'success': success})

# ---------- ADMIN CRUD ----------
def View_Doctor(request):
    if not request.user.is_staff:
        return redirect('login')
    return render(request, 'view_doctor.html', {'doc': Doctor.objects.all()})

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Doctor

def Add_Doctor(request):
    error = ""
    if not request.user.is_staff:
        return redirect('login')

    if request.method == 'POST':
        name = request.POST['name']
        contact = request.POST['contact']
        specialization = request.POST['specialization']
        password = request.POST['password']
        username = request.POST['username']   # unique username for login

        try:
            # 1. Create User account
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=name
            )

            # 2. Create Doctor entry linked to the above user
            Doctor.objects.create(
                user=user,             # make sure your doctor model has user FK
                name=name,
                mobile=contact,
                specialization=specialization
            )

            error = "no"
        except Exception as e:
            print("Error:", e)
            error = "yes"

    return render(request, 'add_doctor.html', {'error': error})


def Delete_Doctor(request, pid):
    if not request.user.is_staff:
        return redirect('login')
    Doctor.objects.filter(id=pid).delete()
    return redirect('view_doctor')

def View_Patient(request):
    if not request.user.is_staff:
        return redirect('login')
    return render(request, 'view_patient.html', {'pat': Patient.objects.all()})

def Add_Patient(request):
    error = ""
    if not request.user.is_staff:
        return redirect('login')
    if request.method == 'POST':
        n = request.POST['name']
        g = request.POST['gender']
        m = request.POST['mobile']
        a = request.POST['address']
        try:
            Patient.objects.create(name=n, gender=g, mobile=m, address=a)
            error = "no"
        except:
            error = "yes"
    return render(request, 'add_patient.html', {'error': error})

def Delete_Patient(request, pid):
    if not request.user.is_staff:
        return redirect('login')
    Patient.objects.filter(id=pid).delete()
    return redirect('view_patient')

def View_Appointment(request):
    if not request.user.is_staff:
        return redirect('login')
    return render(request, 'view_appointment.html', {'appoint': Appointment.objects.all()})

def Add_Appointment(request):
    error = ""
    if not request.user.is_staff:
        return redirect('login')
    doctor1 = Doctor.objects.all()
    patient1 = Patient.objects.all()
    if request.method == 'POST':
        d = request.POST['doctor']
        p = request.POST['patient']
        d1 = request.POST['date']
        t = request.POST['time']
        doctor = Doctor.objects.filter(name=d).first()
        patient = Patient.objects.filter(name=p).first()
        try:
            Appointment.objects.create(doctor=doctor, patient=patient, date1=d1, time1=t)
            error = "no"
        except:
            error = "yes"
    return render(request, 'add_appointment.html', {'doctor': doctor1, 'patient': patient1, 'error': error})

def Delete_Appointment(request, pid):
    if not request.user.is_staff:
        return redirect('login')
    Appointment.objects.filter(id=pid).delete()
    return redirect('view_appointment')


def show_session(request):
    # Example: Set some session data if not set
    if 'visits' in request.session:
        request.session['visits'] += 1
    else:
        request.session['visits'] = 1

    session_data = dict(request.session.items())
    return render(request, 'session_page.html', {'session_data': session_data})

# Page 2: Show Cookies
def show_cookies(request):
    # Example: Set a cookie
    response = render(request, 'cookies_page.html', {'cookies': request.COOKIES})
    if not request.COOKIES.get('my_cookie'):
        response.set_cookie('my_cookie', 'This is a sample cookie', max_age=3600)  # 1 hour
    return response
