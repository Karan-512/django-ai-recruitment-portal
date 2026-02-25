from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from Company.models import CompanyProfile
from django.contrib import messages
from .models import JobPosting
from .models import Application
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from django.db.models import Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

from rest_framework.decorators import api_view
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.paginator import Paginator
from .models import JobPosting
from .serializers import JobPostingSerializer



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
def jobPosting(request, job_id=None):
    company = CompanyProfile.objects.get(user=request.user)

    job = None
    if job_id:
        job = get_object_or_404(JobPosting, id=job_id, company=company)

    if request.method == "POST":

        if job:  # UPDATE
            job.job_title = request.POST.get("job_title")
            job.job_description = request.POST.get("job_description")
            job.salary = request.POST.get("salary")
            job.location = request.POST.get("location")
            job.job_type = request.POST.get("job_type")
            job.required_experience = request.POST.get("required_experience")
            job.skills_required = request.POST.get("skills_required")
            job.deadline = request.POST.get("deadline")

            job.save()
            messages.success(request, "Job updated successfully!")
            return redirect("company-home")

        else:  # CREATE NEW
            JobPosting.objects.create(
                company=company,
                job_title=request.POST.get("job_title"),
                job_description=request.POST.get("job_description"),
                salary=request.POST.get("salary"),
                location=request.POST.get("location"),
                job_type=request.POST.get("job_type"),
                required_experience=request.POST.get("required_experience"),
                skills_required=request.POST.get("skills_required"),
                deadline=request.POST.get("deadline"),
            )

            messages.success(request, "Job posted successfully!")
            return redirect("company-home")

    return render(request, 'jobPosting.html', {
        'pageTitle': "Edit Job" if job else "Post a Job",
        'job': job
    })

# @login_required
# def jobPosting(request):
#     company = CompanyProfile.objects.get(user=request.user)

#     if request.method == "POST":
#         data = request.POST

#         JobPosting.objects.create(
#             company=company,
#             job_title=data.get("job_title"),
#             job_description=data.get("job_description"),
#             salary=data.get("salary"),
#             location=data.get("location"),
#             job_type=data.get("job_type"),
#             required_experience=data.get("required_experience"),
#             skills_required=data.get("skills_required"),
#             deadline=data.get("deadline"),
#         )

#         messages.success(request, "Job posted successfully!")

#         return render(request, 'jobPosting.html', {
#             'pageTitle': "Post a Job"
#         })

#     return render(request, 'jobPosting.html', {
#         'pageTitle': "Post a Job"
#     })

@login_required
def JobDetail(request, job_id):
    company = CompanyProfile.objects.get(user=request.user)

    job = get_object_or_404(
        JobPosting,
        id=job_id,
        company=company  # ensures company sees only its jobs
    )

    return render(request, "job_detail.html", {
        "job": job,
        "pageTitle": "Job Details"
    })



@login_required
def view_applications(request):
    try:
        company_profile = CompanyProfile.objects.get(user=request.user)
    except CompanyProfile.DoesNotExist:
        return redirect('company-profile')

    status = request.GET.get('status', 'all')
    today = timezone.now().date()

    jobs = JobPosting.objects.filter(company=company_profile)

    if status == 'live':
        jobs = jobs.filter(is_active=True, deadline__gte=today)

    elif status == 'closed':
        jobs = jobs.filter(is_active=False)

    elif status == 'expired':
        jobs = jobs.filter(deadline__lt=today)

    jobs = jobs.annotate(applicant_count=Count('applications')).order_by('-posted_date')

    return render(request, 'applications.html', {
        'jobs': jobs,
        'today': today,
        'pageTitle': 'View Applications'
    })


@login_required
def job_applicants(request, job_id):
    company = get_object_or_404(CompanyProfile, user=request.user)

    job = get_object_or_404(JobPosting, id=job_id, company=company)

    applications = Application.objects.filter(job_posting=job)

    return render(request, 'job_applicants.html', {
        'job': job,
        'applications': applications,
        'pageTitle': 'View Applications'
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def job_list_api(request):
    company = CompanyProfile.objects.get(user=request.user)
    jobs = JobPosting.objects.filter(company=company)

    from .serializers import JobPostingSerializer
    serializer = JobPostingSerializer(jobs, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def job_applicants_api(request, job_id):
    job = JobPosting.objects.get(id=job_id)
    applications = Application.objects.filter(job_posting=job)

    from .serializers import ApplicationSerializer
    serializer = ApplicationSerializer(applications, many=True)
    return Response(serializer.data)


# def ViewApplications(request):
#     return render(request, 'applications.html', {'pageTitle': "View Applications"})

@login_required
def ToggleJobStatus(request, job_id):
    company = CompanyProfile.objects.get(user=request.user)
    job = get_object_or_404(JobPosting, id=job_id, company=company)

    job.is_active = not job.is_active
    job.save()

    return redirect("job_detail", job_id=job.id)

@api_view(['GET'])
def get_jobs(request):

    jobs = JobPosting.objects.select_related("company").all().order_by('-posted_date')
    search = request.GET.get("search")
    location = request.GET.get("location")
    job_type = request.GET.get("job_type")

    if search:
        jobs = jobs.filter(job_title__icontains=search)

    if location:
        jobs = jobs.filter(location__icontains=location)

    if job_type:
        jobs = jobs.filter(job_type__iexact=job_type)

    serializer = JobPostingSerializer(jobs, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_job_detail(request, pk):
    job = get_object_or_404(
        JobPosting.objects.select_related('company'),
        pk=pk
    )

    serializer = JobPostingSerializer(job)
    print(serializer.data)
    return Response(serializer.data)
