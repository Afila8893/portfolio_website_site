from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from project.models import Coordinator, Volunteer, Student, Event, AttendanceRecord, Notification, FinancialRecord
from .forms import VolunteerForm, CoordinatorRegistrationForm, CoordinatorLoginForm, VolunteerLoginForm, VolunteerRegistrationForm
from .models import Event,  AttendanceRecord, FinancialRecord

# Predefined Admin Users
ALLOWED_USERS = {
    'admin1': 'password1',
    'admin2': 'password2',
    'admin3': 'password3',
    'admin4': 'password4',
}

def homepage(request):
    return render(request, 'project/homepage.html')


def custom_admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username in ALLOWED_USERS and ALLOWED_USERS[username] == password:
            user, created = User.objects.get_or_create(username=username)
            user.set_password(password)
            user.save()
            login(request, user)
            return redirect('admin_home')
        else:
            error = 'Invalid username or password.'
            return render(request, 'project/admin_login.html', {'error': error})

    return render(request, 'project/admin_login.html')

def green_guardians(request):
    return render(request, 'project/green_guardians.html')

def rural_health_ambassadors(request):
    return render(request, 'project/rural_health_ambassadors.html')

def each_one_teach_one(request):
    return render(request, 'project/each_one.html')

def skillup_saturdays(request):
    return render(request, 'project/skillup.html')

def mission_graam_upliftment(request):
    return render(request, 'project/mission.html')

def disaster_readiness_crew(request):
    return render(request, 'project/disaster.html')
@login_required
def admin_home(request):
    return render(request, 'project/admin_homepage.html')


def register_volunteer(request):
    if request.method == 'POST':
        form = VolunteerForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            if password != confirm_password:
                messages.error(request, "Passwords do not match!")
                return redirect('register_volunteer')

            volunteer = form.save(commit=False)
            volunteer.password = make_password(password)  # ✅ Correct hashing
            volunteer.save()
            messages.success(request, "Volunteer registration successful!")
            return redirect('registration_success')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = VolunteerForm()

    return render(request, 'project/register_volunteer.html', {'form': form})


def register_coordinator(request):
    if request.method == 'POST':
        form = CoordinatorRegistrationForm(request.POST)
        if form.is_valid():
            coordinator = form.save(commit=False)
            coordinator.password = make_password(form.cleaned_data['password'])
            coordinator.save()
            messages.success(request, "Coordinator registration successful!")
            return redirect('registration_success')
    else:
        form = CoordinatorRegistrationForm()

    return render(request, 'project/register_coordinator.html', {'form': form})


def coordinator_login(request):
    if request.method == 'POST':
        form = CoordinatorLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                coordinator = Coordinator.objects.get(username=username)
                if check_password(password, coordinator.password):
                    request.session['coordinator_id'] = coordinator.id
                    messages.success(request, f"Welcome, {coordinator.first_name}!")
                    return redirect('coordinator_dashboard')
                else:
                    messages.error(request, "Invalid password.")
            except Coordinator.DoesNotExist:
                messages.error(request, "Coordinator not found.")
    else:
        form = CoordinatorLoginForm()

    return render(request, 'project/coordinator_login.html', {'form': form})


@login_required
def coordinator_dashboard(request):
    events = Event.objects.all()
    attendance_records =  AttendanceRecord.objects.all()
    financial_records = FinancialRecord.objects.all()
    
    context = {
        'events': events,
        'attendance_records': attendance_records,
        'financial_records': financial_records,
    }
    return render(request, 'project/coordinator_dashboard.html', context)

def registration_success(request):
    return render(request, 'project/registration_success.html')


@login_required
@login_required
def attendance_tracker(request):
    events = Event.objects.all()
    students = Student.objects.all()

    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        student_id = request.POST.get('student_id')
        student_name = request.POST.get('student_name')  # You were missing this!
        status = request.POST.get('attendance')

        if not all([event_id, student_id, student_name, status]):
            messages.error(request, "Please fill all the fields.")
            return redirect('attendance_tracker')

        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            messages.error(request, "Event does not exist.")
            return redirect('attendance_tracker')

        # Save record
        AttendanceRecord.objects.create(
            event=event,
            student_id=student_id,
            name=student_name,
            status=status
        )

        messages.success(request, "Attendance submitted successfully!")
        return redirect('attendance_tracker')

    attendance_records = AttendanceRecord.objects.all().select_related('event')
    return render(request, 'project/attendance_tracker.html', {
        'events': events,
        'students': students,
        'attendance_records': attendance_records,
    })


def upload_event(request):
    if request.method == 'POST':
        name = request.POST.get('name')  # ✅ NOT event_id
        description = request.POST.get('description')
        date = request.POST.get('date')
        time = request.POST.get('time')
        location = request.POST.get('location')
        image = request.FILES.get('image')

        if all([name, description, date, time, location, image]):
            Event.objects.create(
                name=name,
                description=description,
                date=date,
                location=location,
                image=image
            )
            messages.success(request, "Event uploaded successfully!")
        else:
            messages.error(request, "Please fill in all fields.")

        return redirect('upload_event')

    return render(request, 'project/upload_event.html')


def send_notification(request): 
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('message')  # ✅ Use the correct name from form

        if title and content:
            Notification.objects.create(title=title, content=content)
            messages.success(request, "Notification sent successfully!")
            return redirect('send_notification')
        else:
            messages.error(request, "Both title and content are required.")

    return render(request, 'project/send_notification.html')



def financial_record(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        category = request.POST.get('category')

        if all([date, description, amount, category]):
            FinancialRecord.objects.create(
                date=date,
                description=description,
                amount=amount,
                category=category
            )
            messages.success(request, "Record added successfully!")
            return redirect('financial_record')
        else:
            messages.error(request, "All fields are required.")

    transactions = FinancialRecord.objects.order_by('-date')
    return render(request, 'project/financial_record.html', {'transactions': transactions})


def volunteer_login(request):
    if request.method == 'POST':
        form = VolunteerLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                volunteer = Volunteer.objects.get(username=username)
                if check_password(password, volunteer.password):
                    request.session['volunteer_id'] = volunteer.id
                    messages.success(request, f"Welcome, {volunteer.full_name}!")
                    return redirect('volunteer_dashboard')
                else:
                    messages.error(request, "Invalid password.")
            except Volunteer.DoesNotExist:
                messages.error(request, "Volunteer not found.")
    else:
        form = VolunteerLoginForm()

    return render(request, 'project/volunteer_login.html', {'form': form})

def volunteer_dashboard(request):
    volunteer_id = request.session.get('volunteer_id')  # Ensure you store it on login
    if not volunteer_id:
        return redirect('volunteer_login')

    volunteer = Volunteer.objects.get(id=volunteer_id)

    attendance_records = AttendanceRecord.objects.filter(student_id=volunteer.admission_number).select_related('event')
    events = Event.objects.order_by('-date')
    notifications = Notification.objects.order_by('-sent_at')[:5]

    return render(request, 'project/volunteer_dashboard.html', {
        'volunteer': volunteer,
        'attendance_records': attendance_records,
        'events': events,
        'notifications': notifications,  # ✅ Pass to template

    })
from django.shortcuts import render

# NSS Information Page View
def nss_page(request):
    return render(request, 'project/std.html')

def home(request):
    return render(request, 'project/admin_homepage.html')

def about(request):
    return render(request, 'project/about.html')

def services(request):
    return render(request, 'project/services.html')

def contact(request):
    return render(request, 'project/contact.html')

def home(request):
    return render(request, 'homepage.html')
# Volunteer registration view: handles the registration form submission
def volunteer_register(request):
    if request.method == 'POST':
        form = VolunteerRegistrationForm(request.POST)
        if form.is_valid():
            # Process the form data, e.g., save to the database
            form.save()
            # Redirect to a thank you page or display a success message
            return redirect('thank_you')  # Redirect to a 'Thank You' page after successful submission
    else:
        form = VolunteerRegistrationForm()

    return render(request, 'register_volunteer.html', {'form': form})

def alerts(request):
    return render(request, 'project/alert.html')

def profile_view(request):
    volunteer_id = request.session.get('volunteer_id')
    if not volunteer_id:
        return redirect('volunteer_login')

    volunteer = Volunteer.objects.get(id=volunteer_id)
    return render(request, 'project/profile.html', {'volunteer': volunteer})
