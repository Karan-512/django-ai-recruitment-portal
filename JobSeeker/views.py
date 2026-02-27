from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from JobSeeker.serializers import ApplicationSerializer
from .models import JobSeekerProfile,Experience,Education,Project
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from Company.models import Application, JobPosting
from django.db import transaction




@login_required
def my_profile(request):

    profile, created = JobSeekerProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        with transaction.atomic():

            # ---------------- BASIC INFO ----------------
            request.user.first_name = request.POST.get("first_name", "")
            request.user.last_name = request.POST.get("last_name", "")
            request.user.save()

            profile.phone = request.POST.get("phone", "")
            profile.skills = request.POST.get("skills", "")
            profile.save()

            # ---------------- RESUME ----------------
            if request.FILES.get("resume"):
                profile.resume = request.FILES.get("resume")
                profile.save()
            # ---------------- PROFILE IMAGE ----------------
            if request.FILES.get("profile_image"):
                profile.profile_image = request.FILES.get("profile_image")
                profile.save()

            # ---------------- EXPERIENCE ----------------
            Experience.objects.filter(profile=profile).delete()

            roles = request.POST.getlist("exp_role")
            companies = request.POST.getlist("exp_company")
            start_dates = request.POST.getlist("exp_start")
            end_dates = request.POST.getlist("exp_end")
            descriptions = request.POST.getlist("exp_desc")

            for i in range(len(roles)):
                if roles[i]:
                    Experience.objects.create(
                        profile=profile,
                        role=roles[i],
                        company_name=companies[i],
                        start_date=start_dates[i],
                        end_date=end_dates[i] or None,
                        description=descriptions[i]
                    )

            # ---------------- EDUCATION ----------------
            Education.objects.filter(profile=profile).delete()

            degrees = request.POST.getlist("edu_degree")
            institutions = request.POST.getlist("edu_institution")
            fields = request.POST.getlist("edu_field")
            start_years = request.POST.getlist("edu_start")
            end_years = request.POST.getlist("edu_end")

            for i in range(len(degrees)):
                if degrees[i]:
                    Education.objects.create(
                        profile=profile,
                        degree=degrees[i],
                        institution=institutions[i],
                        field_of_study=fields[i],
                        start_year=int(start_years[i]),
                        end_year=int(end_years[i]) if end_years[i] else None
                    )

            # ---------------- PROJECTS ----------------
            Project.objects.filter(profile=profile).delete()

            titles = request.POST.getlist("proj_title")
            descriptions = request.POST.getlist("proj_desc")
            techs = request.POST.getlist("proj_tech")
            links = request.POST.getlist("proj_link")

            for i in range(len(titles)):
                if titles[i]:
                    Project.objects.create(
                        profile=profile,
                        title=titles[i],
                        description=descriptions[i],
                        technologies_used=techs[i],
                        project_link=links[i] or None
                    )
        messages.success(request, "Profile updated successfully!")
        return redirect("js-my-profile")

    context = {
        "profile": profile,
        'pageTitle': 'My Profile'
    }

    return render(request, "my_profile.html", context)


def Home(request):
    return render(request, 'home.html', {'pageTitle': 'Home'})

def MyApplications(request):
    return render(request, "my_applications.html", {'pageTitle' : 'My Applications'})


def job_detail_page(request, pk):
    return render(request, "js_job_detail.html", {"job_id": pk, 'pageTitle': 'Home'})

@api_view(['GET'])
def dashboard_stats(request):

    user = request.user

    try:
        profile = JobSeekerProfile.objects.get(user=user)
    except JobSeekerProfile.DoesNotExist:
        return Response({"error": "Profile not found"}, status=404)

#   Applied Count

    applications = Application.objects.filter(
        job_seeker=profile,
        is_active=True
    )

    applied_count = applications.count()
#   Profile Completion Card

    fields = [
        request.user.first_name,
        request.user.last_name,
        request.user.email,
        profile.phone,
        profile.resume,
        profile.skills,
    ]

    filled_fields = sum(1 for field in fields if field)
    completion_percentage = int((filled_fields / len(fields)) * 100)
    return Response({
        "applied_jobs": applied_count,
        "profile_completion": completion_percentage
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_applications(request):

    applications = Application.objects.filter(
        job_seeker__user=request.user,
        is_active=True
    ).select_related("job_posting", "job_posting__company").order_by("-applied_date")

    serializer = ApplicationSerializer(applications, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def apply_to_job(request, pk):
    job = get_object_or_404(JobPosting, pk=pk)

    try:
        job_seeker = request.user.job_seeker_profile
    except:
        return Response({"error": "Job seeker profile not found"},
                        status=status.HTTP_400_BAD_REQUEST)

    # Prevent duplicate applications
    if Application.objects.filter(
            job_seeker=job_seeker,
            job_posting=job
    ).exists():
        return Response({"error": "Already applied"},
                        status=status.HTTP_400_BAD_REQUEST)

    cover_letter = request.data.get("cover_letter", "")

    Application.objects.create(
        job_seeker=job_seeker,
        job_posting=job,
        cover_letter=cover_letter
    )

    return Response({"message": "Application submitted successfully"})