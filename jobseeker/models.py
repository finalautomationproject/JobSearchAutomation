from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField

class AllJobs(models.Model):
    id = models.AutoField(primary_key=True)
    application_website = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255, blank=True)
    company = models.CharField(max_length=255, blank=True)
    application_url = models.CharField(max_length=400, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

class ScrapedJob(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    job_title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    location = models.TextField()
    application_url = models.CharField(max_length=400)
    created_at = models.DateTimeField(default=timezone.now)

class IndeedJob(models.Model):
    id = models.AutoField(primary_key=True)
    job_title = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=200, blank=True)
    job_description = models.CharField(max_length=300, blank=True)
    application_url = models.CharField(max_length=400, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

class DiceJob(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, default='Untitled')
    company = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=200,blank=True)
    description = models.CharField(max_length=200,blank=True)
    employment_type = models.CharField(max_length=200,blank=True)
    posted_date = models.CharField(max_length=200, blank=True)
    application_url = models.CharField(max_length=400, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

class NaukriJob(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    experience = models.CharField(max_length=100)
    description = models.TextField()
    tags_list = models.CharField(max_length=255)
    posting_date = models.CharField(max_length=255)
    application_url = models.CharField(max_length=400)
    created_at = models.DateTimeField(default=timezone.now)

class ZipRecruiterJob(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    job_title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    application_url = models.CharField(max_length=400)
    created_at = models.DateTimeField(default=timezone.now)

class JobSearchErrors(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    error_instance = models.CharField(max_length=255)
    error = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

class JobSuccess(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    success_instance = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    avatar = models.ImageField(upload_to='userimages/', blank=True)
    linkedin_password = models.CharField(max_length=100)
    indeed_password = models.CharField(max_length=100)
    dice_password = models.CharField(max_length=100)
    profession = models.CharField(max_length=250)
    interests = models.CharField(max_length=255, blank=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    country = CountryField(blank=True)
    location = models.CharField(max_length=100)
    resume = models.FileField(upload_to='documents/', blank=True)

    def __str__(self):
        return self.user.username

