from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from django.db.models.signals import post_save
from django.dispatch import receiver
from Company.models import CompanyProfile
from JobSeeker.models import JobSeekerProfile


User = get_user_model()

def landing_page(request):
    return render(request, 'landing.html')


def login_view(request):

    if request.user.is_authenticated:
        return redirect_by_role(request.user)

    if request.method == "POST":

        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, "Both fields are required!")
            return redirect('login')

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, "Invalid Username or Password")
            return redirect('login')

        login(request, user)
        # messages.success(request, f"Welcome {user.username}!")

        return redirect_by_role(user)

    return render(request, 'login.html')


def signup_view(request):
    if request.method == "POST":
        fname = request.POST.get("first_name")
        lname = request.POST.get("last_name")
        email = request.POST.get("email").lower()
        password = request.POST.get("password1")
        cpass = request.POST.get("password2")
        role = request.POST.get("role")

        if User.objects.filter(username=email).exists():
            return render(request, 'signup.html', {
                "error": "User already exists. Please login."
            })

        if password != cpass:
            return render(request, 'signup.html', {
                "error": "Passwords do not match."
            })

        try:
            User.objects.create_user(
                username=email,
                email=email,
                first_name=fname,
                last_name=lname,
                password=password,
                role=role
            )
        except Exception:
            return render(request, 'signup.html', {
                "error": "Something went wrong. Please try again."
            })

        return redirect('login')

    return render(request, 'signup.html')


def redirect_by_role(user):
    if user.role == 'job_seeker':
        return redirect('js-home')
    elif user.role == 'company':
        return redirect('company-home')
    else:
        return redirect('landing')

@login_required
def logout_view(request):
    logout(request)
    return redirect("landing")


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'company':
            CompanyProfile.objects.create(user=instance)
        elif instance.role == 'job_seeker':
            JobSeekerProfile.objects.create(user=instance)