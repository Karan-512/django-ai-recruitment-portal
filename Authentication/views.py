from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.contrib.auth import get_user_model

from django.contrib.auth import logout

User = get_user_model()

def landing_page(request):
    return render(request, 'landing.html')


def login_view(request):

    if request.user.is_authenticated:
        return redirect_by_role(request.user)

    if request.method == "POST":

        username = request.POST.get('username')
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
        email = request.POST.get("email")
        password = request.POST.get("password1")
        cpass = request.POST.get("password2")
        role = request.POST.get("role")
        obj = User.objects.filter(username = email).exists()
        if obj:
            return render(request,'signup.html',{"error":"User already exists. Please try again!"})
        elif(password != cpass):
            return render(request,'signup.html',{"error":"Passwords don't match!"})
        else:
            User.objects.create_user(
                username=email,
                first_name=fname,
                last_name=lname,
                email=email,
                password=password,
                role=role)
            return redirect('login')
    else:
        return render(request, 'signup.html')


def redirect_by_role(user):
    if user.role == 'job_seeker':
        return redirect('js-my-profile')
    elif user.role == 'company':
        return redirect('landing')
    else:
        return redirect('landing')

@login_required
def logout_view(request):
    logout(request)
    return redirect("landing")
