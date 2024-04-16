# Generated by Django 4.2.9 on 2024-04-16 18:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_countries.fields
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AllJobs',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('application_website', models.CharField(max_length=255)),
                ('job_title', models.CharField(blank=True, max_length=255)),
                ('company', models.CharField(blank=True, max_length=255)),
                ('application_url', models.CharField(blank=True, max_length=400)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='DiceJob',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(default='Untitled', max_length=200)),
                ('company', models.CharField(blank=True, max_length=200)),
                ('location', models.CharField(blank=True, max_length=200)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('employment_type', models.CharField(blank=True, max_length=200)),
                ('posted_date', models.CharField(blank=True, max_length=200)),
                ('application_url', models.CharField(blank=True, max_length=400)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='IndeedJob',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('job_title', models.CharField(max_length=200)),
                ('company_name', models.CharField(blank=True, max_length=200)),
                ('location', models.CharField(blank=True, max_length=200)),
                ('job_description', models.CharField(blank=True, max_length=300)),
                ('application_url', models.CharField(blank=True, max_length=400)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='ZipRecruiterJob',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('job_title', models.CharField(max_length=255)),
                ('company', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('application_url', models.CharField(max_length=400)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('avatar', models.ImageField(blank=True, upload_to='userimages/')),
                ('linkedin_password', models.CharField(max_length=100)),
                ('indeed_password', models.CharField(max_length=100)),
                ('dice_password', models.CharField(max_length=100)),
                ('profession', models.CharField(max_length=250)),
                ('interests', models.CharField(blank=True, max_length=255)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None)),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2)),
                ('location', models.CharField(max_length=100)),
                ('resume', models.FileField(blank=True, upload_to='documents/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ScrapedJob',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('job_title', models.CharField(max_length=255)),
                ('company_name', models.CharField(max_length=255)),
                ('location', models.TextField()),
                ('application_url', models.CharField(max_length=400)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='NaukriJob',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('company', models.CharField(max_length=255)),
                ('experience', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('tags_list', models.CharField(max_length=255)),
                ('posting_date', models.CharField(max_length=255)),
                ('application_url', models.CharField(max_length=400)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='JobSuccess',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('success_instance', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='JobSearchErrors',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('error_instance', models.CharField(max_length=255)),
                ('error', models.TextField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
