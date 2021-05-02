from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User, AbstractUser
from django.contrib.auth import get_user_model

GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other')
]

BLOOD_GROUPS = [
    ('O-', 'O-'),
    ('O+', 'O+'),
    ('A-', 'A-'),
    ('A+', 'A+'),
    ('B-', 'B-'),
    ('B+', 'B+'),
    ('AB-', 'AB-'),
    ('AB+', 'AB+'),
]

USER_CHOICES = [
    ('D', 'Doctor'),
    ('P', 'Patient'),
    ('R', 'Receptionist'),
    ('HR', 'HR')
]

class User(AbstractUser):
    user_type = models.CharField(choices=USER_CHOICES, max_length=2)

    def is_doctor(self):
        if self.user_type == 'D':
            return True
        else:
            return False

    def is_patient(self):
        if self.user_type == 'P':
            return True
        else:
            return False

    def is_receptionist(self):
        if self.user_type == 'R':
            return True
        else:
            return False

    def is_HR(self):
        if self.user_type == 'HR':
            return True
        else:
            return False

    class Meta:
        ordering = ('id',)

User = get_user_model()

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_profile')
    name = models.CharField(max_length=50)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=17)
    user_photo = models.ImageField(upload_to='profile/user_pics',null=True)
    email = models.EmailField()
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1)
    age = models.IntegerField(blank=True, null=True)
    address = models.TextField(max_length=500)
    datefield = models.DateField(null=True)
    blood_group = models.CharField(choices=BLOOD_GROUPS, max_length=3)
    med_reps = models.FileField(upload_to='profile/med_reps', blank=True)
    status = models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], null=True, blank=True, max_length=8)
    agree = models.BooleanField("I agree to the T&C", default=False, blank=False)

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return "Profile for {}".format(self.user)


class Appointment(models.Model):
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed')], max_length=10)
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor')

    def __str__(self):
        return "Patient - {} Doc- {} At {} {}".format(self.patient, self.doctor, self.date, self.time)

class Prescription(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_prescription')
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_prescription')
    date = models.DateField(auto_now_add=True)
    symptoms = models.CharField(max_length=200)
    prescription = models.TextField()

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return "Presciption Doc-{} Patient-{}".format(self.doctor, self.patient)