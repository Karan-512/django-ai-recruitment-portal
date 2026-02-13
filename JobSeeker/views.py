from django.shortcuts import render

# Create your views here.
def myProfile(request):
    return render(request, 'myProfile.html', {'pageTitle': 'My Profile'})

def allJobs(request):
    pass

def savedJobs(request):
    pass

def jobRecommendations(request):
    pass

