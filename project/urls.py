from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('admin-login/', views.custom_admin_login, name='custom_admin_login'),
    path('admin-home/', views.admin_home, name='admin_home'),
    # Volunteer registration page
    path('volunteer_registration/', views.register_volunteer, name='volunteer_registration'),

    # Coordinator registration page
    path('coordinator_registration/', views.register_coordinator, name='register_coordinator'),

    # Registration success page
    path('registration_success/', views.registration_success, name='registration_success'),
    path('coordinator_login/login/', views.coordinator_login, name='coordinator_login'),
    path('coordinator/dashboard/', views.coordinator_dashboard, name='coordinator_dashboard'),
    path('attendance_tracker/', views.attendance_tracker, name='attendance_tracker'),
    path('upload_event/', views.upload_event, name='upload_event'),
    path('send-notification/', views.send_notification, name='send_notification'),
    path('financial-record/', views.financial_record, name='financial_record'),
    path('volunteer/login/', views.volunteer_login, name='volunteer_login'),
    path('volunteer/dashboard/', views.volunteer_dashboard, name='volunteer_dashboard'),
    path('nss/', views.nss_page, name='nss_page'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('', views.home, name='home'),  # This matches with { % url 'home' %} in your template
    path('alerts/', views.alerts, name='alerts'),  # ✅ THIS is what’s missing
    path('volunteer/profile/', views.profile_view, name='profile_view'),  # ✅ Add this line
    path('green-guardians/', views.green_guardians, name='green_guardians'),
    path('rural-health-ambassadors/', views.rural_health_ambassadors, name='rural_health_ambassadors'),
    path('each-one-teach-one/', views.each_one_teach_one, name='each_one_teach_one'),
    path('skillup-saturdays/', views.skillup_saturdays, name='skillup_saturdays'),
    path('mission-graam-upliftment/', views.mission_graam_upliftment, name='mission_graam_upliftment'),
    path('disaster-readiness-crew/', views.disaster_readiness_crew, name='disaster_readiness'),

]
