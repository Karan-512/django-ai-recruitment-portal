from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required

from JobSeeker.serializers import ApplicationSerializer
from .models import JobSeekerProfile,Experience,Education,Project
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from Company.models import Application
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

        return redirect("js-my-profile")

    context = {
        "profile": profile,
        'pageTitle': 'My Profile'
    }

    return render(request, "my_profile.html", context)


# @login_required
# def myProfile(request):
#     user = request.user
#     profile, created = JobSeekerProfile.objects.get_or_create(user=user)

#     if request.method == "POST":
#         card_type = request.POST.get("card_type")

#         if card_type == "basic_info":
#             user.first_name = request.POST.get("first_name", user.first_name)
#             user.last_name = request.POST.get("last_name", user.last_name)
#             user.email = request.POST.get("email", user.email)
#             user.save()

#         elif card_type == "phone":
#             profile.phone = request.POST.get("phone", profile.phone)
#             profile.save()

#         elif card_type == "resume" and 'resume' in request.FILES:
#             profile.resume = request.FILES['resume']
#             profile.save()

#         elif card_type == "experience_add":
#             Experience.objects.create(
#                 profile=profile,
#                 role=request.POST.get("role"),
#                 company_name=request.POST.get("company_name"),
#                 start_date=request.POST.get("start_date"),
#                 end_date=request.POST.get("end_date") or None,
#                 description=request.POST.get("description"),
#             )
#         elif card_type == "experience_delete":
#             exp_id = request.POST.get("exp_id")
#             Experience.objects.filter(id=exp_id, profile=profile).delete()
#         elif card_type == "experience_update":
#             exp_id = request.POST.get("exp_id")
#             exp = get_object_or_404(Experience, id=exp_id, profile=profile)
#             exp.role = request.POST.get("role", exp.role)
#             exp.company_name = request.POST.get("company_name", exp.company_name)
#             exp.start_date = request.POST.get("start_date", exp.start_date)
#             exp.end_date = request.POST.get("end_date") or exp.end_date
#             exp.description = request.POST.get("description", exp.description)
#             exp.save()

#         elif card_type == "project_add":
#             Project.objects.create(
#             profile=profile,
#             title=request.POST.get("title"),
#             description=request.POST.get("description", ""),
#             technologies_used=request.POST.get("technologies_used", ""),
#             project_link=request.POST.get("project_link", ""),
#             )
#         elif card_type == "project_delete":
#             proj_id = request.POST.get("proj_id")
#             Project.objects.filter(id=proj_id, profile=profile).delete()
#         elif card_type == "project_update":
#             proj_id = request.POST.get("proj_id")
#             proj = get_object_or_404(Project, id=proj_id, profile=profile)
#             proj.title = request.POST.get("title", proj.title)
#             proj.description = request.POST.get("description", proj.description)
#             proj.technologies_used = request.POST.get("technologies_used", proj.technologies_used)
#             proj.project_link = request.POST.get("project_link", proj.project_link)
#             proj.save()

#         elif card_type == "education_add":
#             Education.objects.create(
#                 profile=profile,
#                 degree=request.POST.get("degree"),
#                 institution=request.POST.get("institution"),
#                 field_of_study=request.POST.get("field_of_study", ""),
#                 start_year=request.POST.get("start_year"),
#                 end_year=request.POST.get("end_year") or None,
#             )
#         elif card_type == "education_delete":
#             edu_id = request.POST.get("edu_id")
#             Education.objects.filter(id=edu_id, profile=profile).delete()

#         elif card_type == "education_update":
#             edu_id = request.POST.get("edu_id")
#             edu = get_object_or_404(Education, id=edu_id, profile=profile)
#             edu.degree = request.POST.get("degree", edu.degree)
#             edu.institution = request.POST.get("institution", edu.institution)
#             edu.field_of_study = request.POST.get("field_of_study", edu.field_of_study)
#             edu.start_year = request.POST.get("start_year", edu.start_year)
#             edu.end_year = request.POST.get("end_year") or edu.end_year
#             edu.save()

#         return redirect('js-my-profile')

#     context = {
#             'user': user,
#             'profile': profile,
#             'pageTitle': 'My Profile'
#             }
#     return render(request, 'myProfile.html', context)

def Home(request):
    return render(request, 'home.html', {'pageTitle': 'Home'})

def savedJobs(request):
    pass

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
