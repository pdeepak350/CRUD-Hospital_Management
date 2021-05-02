from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.views.generic import ListView ,CreateView
from django.shortcuts import redirect, render
from .forms import * 
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import string
import random


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def home(request):
    return render(request, 'index.html')


def SignUp(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            first_name = user.first_name
            last_name = user.last_name
            name = first_name + ' ' + last_name
            UserProfile.objects.create(name=name, user=user)
            login(request, user)
            return redirect('index.html')
    else:
        form = UserCreateForm()
    return render(request, 'signup.html', {'form': form})

@login_required(login_url='/login/')
def CreateUserProfile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            # try:
            password = User.objects.make_random_password()
            username = profile.name.split()[0] + id_generator()
            user = User.objects.create(username=username, user_type="P")
            user.set_password(password)
            user.save_base(raw=True)
            profile.user = user
            profile.save()
            return redirect('appointment:r_dashboard')
            print("Hello")
            # except:
            #     print("Hey")
            #     redirect('appointment:r_dashboard')
    else:
        form = ProfileUpdateForm()
    return render(request, 'profile_create.html', {'form': form})

@login_required(login_url='/login/')
def UpdatedUserProfile(request):
    user = request.user
    profile = UserProfile.objects.get(user=user)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile:profile')
    else:
        form = ProfileUpdateForm(instance=profile)
    return render(request, 'profile.html', {'form': form, 'user':user})

@login_required(login_url='/login/')
def UpdatedUserProfilePk(request, pk):
    user = User.objects.get(pk=pk)
    profile = UserProfile.objects.get(user=user)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('appointment:r_dashboard')
    else:
        form = ProfileUpdateForm(instance=profile)
    return render(request, 'profile.html', {'form': form, 'user':user})


@login_required(login_url='/login/')
def UpdatedDocProfilePk(request, pk):
    user = User.objects.get(pk=pk)
    profile = UserProfile.objects.get(user=user)
    if request.method == 'POST':
        form = DoctorProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('appointment:hr_dashboard')
    else:
        form = DoctorProfileForm(instance=profile)
    return render(request, 'profile.html', {'form': form, 'user':user})

@login_required(login_url='/login/')
def DeleteUserProfilePk(request, pk):
    user = User.objects.get(pk=pk)
    profile = UserProfile.objects.get(user=user)
    if request.method == 'POST':
        user.delete()
        return redirect('appointment:r_dashboard')
    else:
        return render(request, 'profile_delete.html', {'user':user})


@login_required(login_url='/login/')
def DeleteDocProfilePk(request, pk):
    print("hello")
    user = User.objects.get(pk=pk)
    profile = UserProfile.objects.get(user=user)
    if request.method == 'POST':
        user.delete()
        return redirect('appointment:hr_dashboard')
    else:
        return render(request, 'profile_doc_delete.html', {'user':user})

class AppointmentsForAPatientView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'login'
 
    def get_queryset(self):
        return Appointment.objects.filter(patient=self.request.user)
 
 
class AppointmentsForADoctorView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'login'
 
    def get_queryset(self):
        return Appointment.objects.filter(doctor=self.request.user)
 
 
class MedicalHistoryView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'login'
 
    def get_queryset(self):
        return Prescription.objects.filter(patient=self.request.user)
 
 
class PrescriptionListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'login'
 
    def get_queryset(self):
        return Prescription.objects.filter(doctor=self.request.user)


@login_required(login_url='/login/')
def PrescriptionCreateView(request):
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.doctor = request.user
            prescription.save()
            return redirect('doc-prescriptions')
    else:
        form = PrescriptionForm()
    return render(request, 'prescription_create.html', {'form': form})

@login_required(login_url='/login/')
def AppointmentCreateView(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.save()
            return redirect('r_dashboard')
    else:
        form = AppointmentForm()
    return render(request, 'appointment_create.html', {'form': form})


@login_required(login_url='/login/')
def rdashboard(request):
    if request.method == "GET" and request.user.user_type == "R":
        context = {
            "totalApp" : len(Appointment.objects.all()),
            "compApp" : len(Appointment.objects.filter(status="Completed")),
            "pendApp" : len(Appointment.objects.filter(status="Pending")),
            "app_list" : Appointment.objects.all(),
            "pat_list" : UserProfile.objects.filter(user__user_type="P")[:5]
        }
        return render(request, 'r_dashboard.html', context=context)

@login_required(login_url='/login/')
def hrdashboard(request):
    if request.method == "GET" and request.user.user_type == "HR":
        context = {
            "totalPat" : len(User.objects.filter(user_type="P")),
            "totalDoc" : len(User.objects.filter(user_type="D")),
            "ondutyDoc" : len(UserProfile.objects.filter(status="Active").filter(user__user_type="D")),
            "doc_list" : UserProfile.objects.filter(user__user_type="D")
        }
        return render(request, 'hr_dashboard.html', context=context)

