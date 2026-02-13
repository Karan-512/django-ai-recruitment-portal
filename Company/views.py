from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from Company.models import CompanyProfile
from django.contrib import messages
from .models import JobPosting

# Create your views here.
@login_required
def Home(request):
    return render(request, 'dashboard.html', {'pageTitle': "Company Dashboard"})

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


# @login_required
# def jobPosting(request):
#     return render(request, 'jobPosting.html', {'pageTitle': "Post a Job"})
# from .models import JobPosting
# from Company.models import CompanyProfile
# from django.contrib import messages

@login_required
def jobPosting(request):
    company = CompanyProfile.objects.get(user=request.user)

    if request.method == "POST":
        job_title = request.POST.get("job_title")
        job_description = request.POST.get("job_description")
        salary = request.POST.get("salary")
        location = request.POST.get("location")
        job_type = request.POST.get("job_type")
        required_experience = request.POST.get("required_experience")
        skills_required = request.POST.get("skills_required")
        deadline = request.POST.get("deadline")

        JobPosting.objects.create(
            company=company,
            job_title=job_title,
            job_description=job_description,
            salary=salary,
            location=location,
            job_type=job_type,
            required_experience=required_experience,
            skills_required=skills_required,
            deadline=deadline
        )

        messages.success(request, "Job posted successfully!")
        # return redirect('company-dashboard')  # change if needed
        return redirect('company-home')

    return render(request, 'jobPosting.html', {'pageTitle': "Post a Job"})


@login_required
def ViewApplications(request):
    return render(request, 'applications.html', {'pageTitle': "View Applications"})
