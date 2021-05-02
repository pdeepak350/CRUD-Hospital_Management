from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *

USER_CHOICES = [
    ('D', 'Doctor'),
    ('P', 'Patient'),
    ('R', 'Receptionist'),
    ('HR', 'HR')
]

class UserCreateForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=USER_CHOICES, required=True, widget=forms.RadioSelect)
    class Meta:
        fields = ("first_name", "last_name", "username", "email", "password1", "password2", "user_type")
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Username"
        self.fields["email"].label = "Email address"

class PrescriptionForm(forms.ModelForm):
    
    class Meta:
        model = Prescription
        fields = ('patient', 'symptoms', 'prescription')

    def __init__(self, *args, **kwargs):
        super(PrescriptionForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['patient'].queryset = User.objects.filter(user_type="P")

class ProfileUpdateForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=False, widget=forms.RadioSelect)
    datefield = forms.DateField(widget = forms.DateInput, required=False)
    user_photo = models.ImageField(upload_to='profile/', default='admin.png')
    class Meta:
        model = UserProfile
        fields = ('name', 'user_photo','phone', 'email', 'gender', 'age', 'address', 'datefield', 'blood_group', 'med_reps', 'agree')


class DoctorProfileForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=False, widget=forms.RadioSelect)
    datefield = forms.DateField(widget = forms.DateInput, required=False)
    user_photo = models.ImageField(upload_to='profile/', default='admin.png')
    class Meta:
        model = UserProfile
        fields = ('name', 'user_photo','phone', 'email', 'gender', 'age', 'address', 'datefield', 'blood_group', 'med_reps', 'agree')
   

class AppointmentForm(forms.ModelForm):

    class Meta:
        model = Appointment
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['patient'].queryset = User.objects.filter(user_type="P")
            self.fields['doctor'].queryset = User.objects.filter(user_type="D")
            self.fields["date"].label = "Date (YYYY-MM-DD)"
            self.fields["time"].label = "Time 24 hr (HH:MM)"