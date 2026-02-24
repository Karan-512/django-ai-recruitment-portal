from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import JobSeekerProfile,Experience,Education,Project

@login_required
def myProfile(request):
    user = request.user
    profile, created = JobSeekerProfile.objects.get_or_create(user=user)

    if request.method == "POST":
        card_type = request.POST.get("card_type")

        if card_type == "basic_info":
            user.first_name = request.POST.get("first_name", user.first_name)
            user.last_name = request.POST.get("last_name", user.last_name)
            user.email = request.POST.get("email", user.email)
           
            user.save()

        elif card_type == "phone":
            profile.phone = request.POST.get("phone", profile.phone)
            profile.save()

        elif card_type == "resume" and 'resume' in request.FILES:
            
            profile.resume = request.FILES['resume']
            profile.save()

        elif card_type == "experience_add":
            Experience.objects.create(
                profile=profile,
                role=request.POST.get("role"),
                company_name=request.POST.get("company_name"),
                start_date=request.POST.get("start_date"),
                end_date=request.POST.get("end_date") or None,
                description=request.POST.get("description"),
            )
        elif card_type == "experience_delete":
            exp_id = request.POST.get("exp_id")
            Experience.objects.filter(id=exp_id, profile=profile).delete()
        elif card_type == "experience_update":
            exp_id = request.POST.get("exp_id")
            exp = get_object_or_404(Experience, id=exp_id, profile=profile)
            exp.role = request.POST.get("role", exp.role)
            exp.company_name = request.POST.get("company_name", exp.company_name)
            exp.start_date = request.POST.get("start_date", exp.start_date)
            exp.end_date = request.POST.get("end_date") or exp.end_date
            exp.description = request.POST.get("description", exp.description)
            exp.save()

        elif card_type == "project_add":
            Project.objects.create(
            profile=profile,
            title=request.POST.get("title"),
            description=request.POST.get("description", ""),
            technologies_used=request.POST.get("technologies_used", ""),
            project_link=request.POST.get("project_link", ""),  
            )
        elif card_type == "project_delete":
            proj_id = request.POST.get("proj_id")
            Project.objects.filter(id=proj_id, profile=profile).delete()
        elif card_type == "project_update":
            proj_id = request.POST.get("proj_id")
            proj = get_object_or_404(Project, id=proj_id, profile=profile)
            proj.title = request.POST.get("title", proj.title)
            proj.description = request.POST.get("description", proj.description)
            proj.technologies_used = request.POST.get("technologies_used", proj.technologies_used)
            proj.project_link = request.POST.get("project_link", proj.project_link)
            proj.save()

        elif card_type == "education_add":
            Education.objects.create(
                profile=profile,
                degree=request.POST.get("degree"),
                institution=request.POST.get("institution"),
                field_of_study=request.POST.get("field_of_study", ""), 
                start_year=request.POST.get("start_year"),
                end_year=request.POST.get("end_year") or None,
            )
        elif card_type == "education_delete":
            edu_id = request.POST.get("edu_id")
            Education.objects.filter(id=edu_id, profile=profile).delete()
            
        elif card_type == "education_update":
            edu_id = request.POST.get("edu_id")
            edu = get_object_or_404(Education, id=edu_id, profile=profile)
            edu.degree = request.POST.get("degree", edu.degree)
            edu.institution = request.POST.get("institution", edu.institution)
            edu.field_of_study = request.POST.get("field_of_study", edu.field_of_study) 
            edu.start_year = request.POST.get("start_year", edu.start_year)
            edu.end_year = request.POST.get("end_year") or edu.end_year
            edu.save()

        return redirect('js-my-profile')

    context = {
            'user': user,
            'profile': profile
            }
    return render(request, 'myProfile.html', context)

def allJobs(request):
    pass

def savedJobs(request):
    pass

def jobRecommendations(request):
    pass