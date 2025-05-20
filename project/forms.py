from django import forms
from .models import Volunteer, Coordinator

class VolunteerForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Volunteer
        fields = ['full_name', 'nss_unit_number', 'admission_number',
                  'mobile_number', 'email_id', 'address', 'blood_group',
                  'class_advisor', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

class CoordinatorRegistrationForm(forms.ModelForm):
    class Meta:
        model = Coordinator
        fields = '__all__'

class CoordinatorLoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
class VolunteerLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class VolunteerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Volunteer
        fields = ['name', 'email', 'skills_interests']
    
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Your full name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'you@example.com'}))
    skills_interests = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'What skills or interests do you have for volunteering?'}))

