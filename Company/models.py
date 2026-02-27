from django.db import models
from django.conf import settings

from JobSeeker.models import JobSeekerProfile

# Create your models here.

class CompanyProfile(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="company_profiles"
    )

    company_name = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    company_logo = models.ImageField(upload_to="company_logos/", blank=True, null=True)
    industry = models.CharField(max_length=150, blank=True)
    company_website = models.URLField(blank=True, null=True)
    company_size = models.CharField(max_length=100, blank=True, null=True)
    founded_year = models.PositiveIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name

class JobPosting(models.Model):

    JOB_TYPE_CHOICES = (
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('remote', 'Remote'),
    )

    company = models.ForeignKey(
        CompanyProfile,
        on_delete=models.CASCADE,
        related_name="job_postings"
    )

    job_title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    job_description = models.TextField(blank=True)

    salary = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    job_type = models.CharField(
        max_length=50,
        choices=JOB_TYPE_CHOICES
    )

    required_experience = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    skills_required = models.CharField(
        max_length=300,
        blank=True,
        null=True
    )

    deadline = models.DateField()

    is_active = models.BooleanField(default=True)

    posted_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.job_title


class Application(models.Model):

    STATUS_CHOICES = (
        ('Applied', 'Applied'),
        ('Reviewing', 'Reviewing'),
        ('Shortlisted', 'Shortlisted'),
        ('Rejected', 'Rejected'),
        ('Accepted', 'Accepted'),
    )

    job_seeker = models.ForeignKey(
        JobSeekerProfile,
        on_delete=models.CASCADE,
        related_name="applications"
    )

    job_posting = models.ForeignKey(
        JobPosting,
        on_delete=models.CASCADE,
        related_name="applications"
    )

    application_status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='applied'
    )

    applied_date = models.DateTimeField(auto_now_add=True)

    cover_letter = models.TextField(blank=True, null=True)

    # created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('job_seeker', 'job_posting')

    def __str__(self):
        return f"{self.job_seeker} - {self.job_posting}"
