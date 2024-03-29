# Generated by Django 4.2.9 on 2024-03-15 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobseeker', '0006_alter_dicejob_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alljobs',
            name='application_url',
            field=models.CharField(blank=True, max_length=400),
        ),
        migrations.AlterField(
            model_name='alljobs',
            name='job_title',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='indeedjob',
            name='application_url',
            field=models.CharField(blank=True, max_length=400),
        ),
        migrations.AlterField(
            model_name='indeedjob',
            name='company_name',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='indeedjob',
            name='job_description',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='indeedjob',
            name='location',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
