from django.db import models
import uuid

# Create your models here.

class Patient(models.Model):
    
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)  
    password = models.CharField(max_length=16)
    gender = models.CharField(max_length=10)
    phonenumber = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    birthdate = models.DateField()
    bloodgroup = models.CharField(max_length=5)


   
    def __str__(self):
        return self.name


class Doctor(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=16)
    gender = models.CharField(max_length=10)
    phonenumber = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    birthdate = models.DateField()
    specialization = models.CharField(max_length=50)
    qualification = models.CharField(max_length=15,null='False',default="MBBS")
    nmc = models.IntegerField(unique=True, null=True)
    doc_image = models.ImageField(upload_to='doc_image',null=True, blank=True)
    doc_license_image = models.ImageField(upload_to='doc_license_image',null=True, blank=True)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    appointment_id = models.UUIDField(default=uuid.uuid4, unique=True)
    doctorname = models.CharField(max_length=50)
    doctoremail = models.EmailField(max_length=50)
    patientname = models.CharField(max_length=50)
    patientemail = models.EmailField(max_length=50)
    appointmentdate = models.DateField(max_length=10)
    appointmenttime = models.TimeField(max_length=10)
    symptoms = models.CharField(max_length=100)
    status = models.BooleanField()
    prescription = models.CharField(max_length=200)

    def __str__(self):
        return self.patientname+" you have appointment with "+self.doctorname
