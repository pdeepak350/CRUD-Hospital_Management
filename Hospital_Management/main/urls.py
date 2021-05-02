from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("login/", auth_views.LoginView.as_view(template_name="login.html"),name='login'),
    path("logout/", auth_views.LogoutView.as_view(template_name="logout.html"), name="logout"),
    path("register/", views.SignUp, name="signup"),
    #########################################
    path("appointments/p/", views.AppointmentsForAPatientView.as_view(), name="patient-appointments"),
    path("appointments/d/", views.AppointmentsForADoctorView.as_view(), name="doctor-appointments"),
    path("medHistory/", views.MedicalHistoryView.as_view(), name="med-history"),
    path("prescriptions/", views.PrescriptionListView.as_view(), name="doc-prescriptions"),
    path("prescription/create", views.PrescriptionCreateView, name="doc-prescriptions-create"),
    path("appointment/create", views.AppointmentCreateView, name="appointment-create"),
    path("rdashboard/", views.rdashboard, name="r_dashboard"),
    path("hrdashboard/", views.hrdashboard, name="hr_dashboard"),
    ######################################
    path("profile/", views.UpdatedUserProfile, name="profile"),
    path("profile/create/", views.CreateUserProfile, name="profile-create"),
    path("profile/<int:pk>/", views.UpdatedUserProfilePk, name="profile-pk"),
    path("profile/doc/<int:pk>/", views.UpdatedDocProfilePk, name="doc-profile-pk"),
    path("profile/<int:pk>/delete/", views.DeleteUserProfilePk, name="profile-delete"),
    path("profile/doc/<int:pk>/delete/", views.DeleteDocProfilePk, name="doc-profile-delete"),
]