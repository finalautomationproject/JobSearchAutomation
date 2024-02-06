from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class ScrapedJob(models.Model):
    job_title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    job_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    
class IndeedJob(models.Model):
    jobinfo = models.CharField(max_length=500)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    linkedin_password = models.CharField(max_length=100)
    indeed_password = models.CharField(max_length=100)
    keywords = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=100)
    resume = models.FileField(upload_to='documents/', blank=True)

    def __str__(self):
        return self.user.username
    

