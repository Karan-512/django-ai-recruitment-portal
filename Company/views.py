from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from Company.models import CompanyProfile
from django.contrib import messages

# Create your views here.
@login_required
def Home(request):
    return render(request, 'dashboard.html', {'pageTitle': "Company Dashboard"})

@login_required
def Profile(request):
    company = CompanyProfile.objects.get(user=request.user)
    print(company.company_logo.url)
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
    return render(request, 'jobPosting.html', {'pageTitle': "Post a Job"})

@login_required
def ViewApplications(request):
    return render(request, 'applications.html', {'pageTitle': "View Applications"})
