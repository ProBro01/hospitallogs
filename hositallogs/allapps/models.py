from django.db import models
from django.core.validators import MaxLengthValidator, MinValueValidator

class Location(models.Model):
    address = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    Pincode = models.PositiveIntegerField()

class Hospital(models.Model):
    name = models.CharField(max_length=30)
    Location = models.ForeignKey(Location, on_delete=models.CASCADE)
    numberofbeds = models.IntegerField(null=True)
    hospitalimage = models.ImageField(upload_to="hospitalimage")
    emailid = models.EmailField(null=True)
    ratings = models.IntegerField(null=True)    
    fees = models.PositiveIntegerField(null=True)
    password = models.CharField(null=True, max_length=20)
    username = models.CharField(null=True, max_length=30)
    discriptions = models.TextField(blank=True, null=True)
    # searchstring = models.TextField(blank=True, null=True)

class Doctor(models.Model):
    Name = models.CharField(max_length=30)
    picture = models.ImageField(upload_to="doctorImages", blank=True, null=True)
    Qualification = models.CharField(max_length=30)
    Specilization = models.CharField(max_length=30)
    experience = models.CharField(max_length=30)
    startingtime = models.TimeField(max_length=30)
    endingtime = models.TimeField()
    ratings = models.IntegerField(null=True, blank=True)
    hospital = models.ForeignKey(Hospital, blank=True, null=True, on_delete=models.CASCADE)
    password = models.CharField(null=True, max_length=20, blank=True)
    username = models.CharField(null=True, max_length=30, blank=True)

class sessions(models.Model):
    sessionToken = models.CharField(max_length=20)
    user = models.ForeignKey(Hospital, on_delete=models.CASCADE, null=True, blank=True)
    is_login = models.BooleanField(null=True)
    is_semiauthentic = models.BooleanField(null=True, default=False)
    otp = models.PositiveIntegerField(validators=[MinValueValidator(111111), MaxLengthValidator(999999)], null=True)

class resetids(models.Model):
    resetid = models.CharField(max_length=20)
    emailid = models.CharField(max_length=25)
    user = models.ForeignKey(Hospital, on_delete=models.CASCADE, null=True)