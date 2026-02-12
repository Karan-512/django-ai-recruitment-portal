from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def Home(request):
    return render(request, 'dashboard.html', {'pageTitle': "Company Dashboard"})

@login_required
def Profile(request):
    return render(request, 'profile.html', {'pageTitle': "Company Profile"})


@login_required
def jobPosting(request):
    return render(request, 'jobPosting.html', {'pageTitle': "Post a Job"})

@login_required
def ViewApplications(request):
    return render(request, 'applications.html', {'pageTitle': "View Applications"})
