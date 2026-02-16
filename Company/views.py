from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from Company.models import CompanyProfile
from django.contrib import messages
from .models import JobPosting
from .models import Application
from django.utils import timezone

# Create your views here.
@login_required
def Home(request):
    try:
        company = CompanyProfile.objects.get(user=request.user)
    except CompanyProfile.DoesNotExist:
        messages.error(request, "Company profile not found.")
        return redirect("login")

    # Get company jobs
    jobs = company.job_postings.all()

    for job in jobs:
        time_diff = timezone.now() - job.posted_date
        total_seconds = int(time_diff.total_seconds())

        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        days = hours // 24

        # ✅ Auto convert
        if hours < 24:
            job.time_display = f"{hours}hr : {minutes:02d} min"
        else:
            if days == 1:
                job.time_display = "1 day"
            else:
                job.time_display = f"{days} days"
    # Counts
    total_jobs = jobs.count()
    total_applications = Application.objects.filter(
        job_posting__company=company
    ).count()

    shortlisted_count = Application.objects.filter(
        job_posting__company=company,
        application_status="shortlisted"   # Make sure this matches your model
    ).count()

    context = {
        "pageTitle": "Company Dashboard",
        "total_jobs": total_jobs,
        "total_applications": total_applications,
        "shortlisted_count": shortlisted_count,
        "jobs": jobs,  # Needed for your carousel
    }

    return render(request, "dashboard.html", context)

@login_required
def Profile(request):
    company = CompanyProfile.objects.get(user=request.user)
    if request.method == 'POST':
        company.company_name = request.POST.get("company_name")
        company.industry = request.POST.get("industry")
        company.company_website = request.POST.get("company_website")
        company.location = request.POST.get("location")
        company.company_size = request.POST.get("company_size")
        company.founded_year = request.POST.get("founded_year")
        company.description = request.POST.get("description")

        if request.FILES.get("company_logo"):
            company.company_logo = request.FILES.get("company_logo")

        company.save()

        messages.success(request, "Company details updated successfully.")
        return redirect('company-profile')
    else:
        return render(request, 'profile.html', {'pageTitle': "Company Profile", 'company': company, 'company_email': request.user.email})



@login_required
def jobPosting(request):
    company = CompanyProfile.objects.get(user=request.user)

    if request.method == "POST":
        data = request.POST

        JobPosting.objects.create(
            company=company,
            job_title=data.get("job_title"),
            job_description=data.get("job_description"),
            salary=data.get("salary"),
            location=data.get("location"),
            job_type=data.get("job_type"),
            required_experience=data.get("required_experience"),
            skills_required=data.get("skills_required"),
            deadline=data.get("deadline"),
        )

        messages.success(request, "Job posted successfully!")

        return render(request, 'jobPosting.html', {
            'pageTitle': "Post a Job"
        })

    return render(request, 'jobPosting.html', {
        'pageTitle': "Post a Job"
    })


@login_required
def ViewApplications(request):
    return render(request, 'applications.html', {'pageTitle': "View Applications"})
