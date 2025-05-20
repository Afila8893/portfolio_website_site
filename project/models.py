from django.db import models
from django.contrib.auth.models import User  # Import User model to use set_password()
import datetime
from django.contrib.auth.hashers import make_password, check_password


class Volunteer(models.Model):
    full_name = models.CharField(max_length=200, default='Unknown')
    nss_unit_number = models.CharField(max_length=100)
    admission_number = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=100, default='UNKNOWN')
    course = models.CharField(max_length=200, default='Unknown')
    mobile_number = models.CharField(max_length=15)
    email_id = models.EmailField(max_length=200, blank=True, null=True)
    address = models.TextField(default='Not provided')
    date_of_birth = models.CharField(max_length=15, default="Not Provided")
    blood_group = models.CharField(max_length=5, default='Not provided')
    class_advisor = models.CharField(max_length=200, default='Not assigned')
    username = models.CharField(max_length=150, unique=True, default='default_username')
    password = models.CharField(max_length=255, default='')
    
    def __str__(self):
        return self.full_name

    def set_password(self, raw_password):
        # Hash and set password using Django's built-in method
        self.password = make_password(raw_password)  # `make_password` hashes the password

    def check_password(self, raw_password):
        # Check the password using Django's built-in password check mechanism
        return check_password(raw_password, self.password)  # `check_password` verifies the hashed password


class Coordinator(models.Model):
    first_name = models.CharField(max_length=100)
    nss_unit = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    address = models.TextField()
    date_of_birth = models.CharField(max_length=15, default="Not Provided")
    username = models.CharField(max_length=150, unique=True, default='default_username')
    password = models.CharField(max_length=255)
    confirm_password = models.CharField(max_length=255)

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = "Coordinator"
        verbose_name_plural = "Coordinators"

    def set_password(self, raw_password):
        # Hash and set password using Django's built-in method
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        # Check the password using Django's built-in password check mechanism
        return check_password(raw_password, self.password)

# models.py
class Student(models.Model):
    student_id = models.CharField(max_length=100, unique=True)
    student_name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.student_name} ({self.student_id})"


class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default="No description provided")
    date = models.DateField()
    time = models.TimeField(default="00:00")  # Add time field
    location = models.CharField(max_length=255, default="No location provided")
    image = models.ImageField(upload_to='events/', null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.date} {self.time.strftime('%H:%M')}"

class AttendanceRecord(models.Model):
    ATTENDANCE_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attendance_records')
    student_id = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=ATTENDANCE_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.student_id}) - {self.event.name} - {self.status}"

    
class Notification(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title    
    

class FinancialRecord(models.Model):
    CATEGORY_CHOICES = [
        ('Income', 'Income'),
        ('Expense', 'Expense'),
        ('Donation', 'Donation'),
        ('Misc', 'Misc'),
    ]

    date = models.DateField()
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    def __str__(self):
        return f"{self.date} - {self.description} - {self.amount}"
