from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from Company.models import CompanyProfile
from django.contrib import messages
from .models import JobPosting
from .models import Application

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
